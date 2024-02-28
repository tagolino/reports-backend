import logging

from dateutil.relativedelta import relativedelta
from django.db.models import Max, Min, Q, Sum
from django.utils import timezone
from sources.customer_portal.enums import ElectricityBillStatusEnum
from sources.customer_portal.models import (
    CustomerPortalECA,
    CustomerPortalElectricityBillMeter,
    CustomerPortalElectricityContract,
)
from sources.data_service.models import DataServiceContract

from celery import shared_task

from .models import BillingDetail, Invoice, MeterInvoice
from .utils import get_electricity_charges

logger = logging.getLogger(__name__)


@shared_task
def create_customer_invoice(invoice_id) -> None:
    invoice = Invoice.objects.get(pk=invoice_id)
    today = timezone.now()

    try:
        electricity_customer_account = CustomerPortalECA.objects.get(
            pk=invoice.electricity_customer_account.customer_portal_eca_id
        )
    except CustomerPortalECA.DoesNotExist:
        return

    meters_consumption = electricity_customer_account.active_meters.annotate(
        day_consumption=Sum(
            "consumptions__consumption",
            filter=Q(
                consumptions__created_at__date__gte=invoice.period_start_at.date(),
                consumptions__created_at__date__lte=invoice.period_end_at.date(),
                consumptions__created_at__time__gt="07:00",
            ),
        ),
        night_consumption=Sum(
            "consumptions__consumption",
            filter=Q(
                consumptions__created_at__date__gte=invoice.period_start_at.date(),
                consumptions__created_at__date__lte=invoice.period_end_at.date(),
                consumptions__created_at__time__gte="00:00",
                consumptions__created_at__time__lte="07:00",
            ),
        ),
        consumption=Sum(
            "consumptions__consumption",
            filter=Q(
                consumptions__created_at__date__gte=invoice.period_start_at.date(),
                consumptions__created_at__date__lte=invoice.period_end_at.date(),
            ),
        ),
        day_cost=Sum(
            "consumptions__cost",
            filter=Q(
                consumptions__created_at__date__gte=invoice.period_start_at.date(),
                consumptions__created_at__date__lte=invoice.period_end_at.date(),
                consumptions__created_at__time__gt="07:00",
            ),
        ),
        night_cost=Sum(
            "consumptions__cost",
            filter=Q(
                consumptions__created_at__date__gte=invoice.period_start_at.date(),
                consumptions__created_at__date__lte=invoice.period_end_at.date(),
                consumptions__created_at__time__gte="00:00",
                consumptions__created_at__time__lte="07:00",
            ),
        ),
        cost=Sum(
            "consumptions__cost",
            filter=Q(
                consumptions__created_at__date__gte=invoice.period_start_at.date(),
                consumptions__created_at__date__lte=invoice.period_end_at.date(),
            ),
        ),
        opening_reading=Min(
            "consumptions__reading",
            filter=Q(
                consumptions__created_at__date__gte=invoice.period_start_at.date(),
                consumptions__created_at__date__lte=invoice.period_end_at.date(),
            ),
        ),
        opening_reading_at=Min(
            "consumptions__created_at",
            filter=Q(
                consumptions__created_at__date__gte=invoice.period_start_at.date(),
                consumptions__created_at__date__lte=invoice.period_end_at.date(),
            ),
        ),
        last_reading=Max(
            "consumptions__reading",
            filter=Q(
                consumptions__created_at__date__gte=invoice.period_start_at.date(),
                consumptions__created_at__date__lte=invoice.period_end_at.date(),
            ),
        ),
        last_reading_at=Max(
            "consumptions__created_at",
            filter=Q(
                consumptions__created_at__date__gte=invoice.period_start_at.date(),
                consumptions__created_at__date__lte=invoice.period_end_at.date(),
            ),
        ),
    )

    for index, meter in enumerate(meters_consumption):
        logger.debug(f"PROCESSING METER: {index} -- {meter.id}")
        active_contracts = CustomerPortalElectricityContract.objects.filter(
            is_active=True,
            end_date__gt=today,
            account__active_meters__pk=meter.id,
        ).distinct()
        if active_contracts.exists():
            for contract in active_contracts:
                try:
                    data_service_contract = DataServiceContract.objects.get(
                        customer__customer_portal_id=invoice.customer.customer_portal_id,
                        name=contract.name,
                    )
                except (
                    DataServiceContract.DoesNotExist,
                    DataServiceContract.MultipleObjectsReturned,
                ) as e:
                    logger.error(
                        f"Contract exception for MPAN: {meter.mpan.mpan} -- {e}"
                    )
                    continue

                contract_name = data_service_contract.name.replace("-", "")
                invoice_number = f"{contract_name}{today:%y%m}-{index + 1}"

                customer_billing_details = BillingDetail.objects.create(
                    invoice_number=invoice_number,
                    billing_name=electricity_customer_account.name,
                    site_name=getattr(meter.asset, "name", ""),
                    site_address=getattr(meter.asset, "address", ""),
                    account_number=contract.name,
                    msn=getattr(meter.device, "serial_number", ""),
                    mpan=getattr(meter.mpan, "mpan", ""),
                    invoice_at=today,
                    bill_from_at=invoice.period_start_at,
                    bill_to_at=invoice.period_end_at,
                    contract_end_at=contract.end_date,
                    payment_due_at=invoice.period_end_at
                    + relativedelta(days=15),
                )

                previous_bill = (
                    CustomerPortalElectricityBillMeter.objects.filter(
                        meter=meter,
                        bill__status__in=[
                            ElectricityBillStatusEnum.PENDING,
                            ElectricityBillStatusEnum.OVERDUE,
                        ],
                    ).aggregate(previous_amount=Sum("total"))
                )

                meter_invoice = MeterInvoice.objects.create(
                    invoice=invoice,
                    customer_billing_details=customer_billing_details,
                    previous_balance=previous_bill.get("previous_amount") or 0,
                    bill_amount=meter.cost or 0,
                    total_amount=previous_bill.get("previous_amount", 0)
                    + meter.cost
                    or 0,
                )
                meter_invoice.save()

                get_electricity_charges(
                    meter, meter_invoice, data_service_contract
                )
