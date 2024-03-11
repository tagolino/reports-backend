from collections import OrderedDict
from copy import deepcopy
from datetime import datetime

from django.db.models import DecimalField, Q, Sum
from django.db.models.functions import Coalesce
from invoices.models import (
    HHConsumptionCharges,
    IndustryCharges,
    MeterInvoice,
    ReadingConsumptionCharges,
)
from openpyxl.worksheet.worksheet import Worksheet
from sources.billing_service.models import (
    BillingServiceContract,
    BillingServiceContractMeter,
    BillingServiceMeter,
)

INVOICE_EXCEL_COLUMNS = OrderedDict(
    {
        "Billing Name": "billing_name",
        "Billing Address": "billing_address",
        "Site Name": "site_name",
        "Site Address": "site_address",
        "VAT No": "vat_number",
        "Account Number": "account_number",
        "MSN": "msn",
        "PC": "pc",
        "MTC": "mtc",
        "LF": "llf",
        "MPAN": "mpan",
        "Contract End Date": "contract_end_at",
        "Invoice Number": "invoice_number",
        "Invoice Date": "invoice_at",
        "Bill From": "bill_from_at",
        "Bill To": "bill_to_at",
        "Payment Due Date": "payment_due_at",
        "Day Consumption - Value": "day_consumption_value",
        "Day Consumption - Unit": "day_consumption_unit",
        "Day Rate - Value": "day_rate_value",
        "Day Rate - Unit": "day_rate_unit",
        "Day Charges": "day_charges",
        "Night Consumption - Value": "night_consumption_value",
        "Night Consumption - Unit": "night_consumption_unit",
        "Night Rate - Value": "night_rate_value",
        "Night Rate - Unit": "night_rate_unit",
        "Night Charges": "night_charges",
        "Opening Reading": "opening_reading",
        "Opening Reading Type": "opening_reading_type",
        "Opening Reading Date": "opening_reading_date",
        "Last Reading": "last_reading",
        "Last Reading Type": "last_reading_type",
        "Last Reading Date": "last_reading_date",
        "Consumption": "consumption",
        "Rate": "rate",
        "Total Electricity Charges": "total_electricity_charges",
        "Industry Charges 1 - Name": "industry_charge_1_name",
        "I.C 1 Quantity 1 - Value": "industry_charge_1_quantity_1_value",
        "I.C 1 Quantity 1 - Unit": "industry_charge_1_quantity_1_unit",
        "I.C 1 Quantity 2 - Value": "industry_charge_1_quantity_2_value",
        "I.C 1 Quantity 2 - Unit": "industry_charge_1_quantity_2_unit",
        "I.C 1 Unit": "industry_charge_1_unit",
        "I.C 1 Rate - Value": "industry_charge_1_rate_value",
        "I.C 1 Rate - Unit": "industry_charge_1_rate_unit",
        "I.C 1 Charges": "industry_charge_1_charges",
        "Industry Charges 2 - Name": "industry_charge_2_name",
        "I.C 2 Quantity 1 - Value": "industry_charge_2_quantity_1_value",
        "I.C 2 Quantity 1 - Unit": "industry_charge_2_quantity_1_unit",
        "I.C 2 Quantity 2 - Value": "industry_charge_2_quantity_2_value",
        "I.C 2 Quantity 2 - Unit": "industry_charge_2_quantity_2_unit",
        "I.C 2 Unit": "industry_charge_2_unit",
        "I.C 2 Rate - Value": "industry_charge_2_rate_value",
        "I.C 2 Rate - Unit": "industry_charge_2_rate_unit",
        "I.C 2 Charges": "industry_charge_2_charges",
        "Industry Charges 3 - Name": "industry_charge_3_name",
        "I.C 3 Quantity 1 - Value": "industry_charge_3_quantity_1_value",
        "I.C 3 Quantity 1 - Unit": "industry_charge_3_quantity_1_unit",
        "I.C 3 Quantity 2 - Value": "industry_charge_3_quantity_2_value",
        "I.C 3 Quantity 2 - Unit": "industry_charge_3_quantity_2_unit",
        "I.C 3 Unit": "industry_charge_3_unit",
        "I.C 3 Rate - Value": "industry_charge_3_rate_value",
        "I.C 3 Rate - Unit": "industry_charge_3_rate_unit",
        "I.C 3 Charges": "industry_charge_3_charges",
        "Industry Charges 4 - Name": "industry_charge_4_name",
        "I.C 4 Quantity 1 - Value": "industry_charge_4_quantity_1_value",
        "I.C 4 Quantity 1 - Unit": "industry_charge_4_quantity_1_unit",
        "I.C 4 Quantity 2 - Value": "industry_charge_4_quantity_2_value",
        "I.C 4 Quantity 2 - Unit": "industry_charge_4_quantity_2_unit",
        "I.C 4 Unit": "industry_charge_4_unit",
        "I.C 4 Rate - Value": "industry_charge_4_rate_value",
        "I.C 4 Rate - Unit": "industry_charge_4_rate_unit",
        "I.C 4 Charges": "industry_charge_4_charges",
        "Industry Charges 5 - Name": "industry_charge_5_name",
        "I.C 5 Quantity 1 - Value": "industry_charge_5_quantity_1_value",
        "I.C 5 Quantity 1 - Unit": "industry_charge_5_quantity_1_unit",
        "I.C 5 Quantity 2 - Value": "industry_charge_5_quantity_2_value",
        "I.C 5 Quantity 2 - Unit": "industry_charge_5_quantity_2_unit",
        "I.C 5 Unit": "industry_charge_5_unit",
        "I.C 5 Rate - Value": "industry_charge_5_rate_value",
        "I.C 5 Rate - Unit": "industry_charge_5_rate_unit",
        "I.C 5 Charges": "industry_charge_5_charges",
        "Industry Charges 6 - Name": "industry_charge_6_name",
        "I.C 6 Quantity 1 - Value": "industry_charge_6_quantity_1_value",
        "I.C 6 Quantity 1 - Unit": "industry_charge_6_quantity_1_unit",
        "I.C 6 Quantity 2 - Value": "industry_charge_6_quantity_2_value",
        "I.C 6 Quantity 2 - Unit": "industry_charge_6_quantity_2_unit",
        "I.C 6 Unit": "industry_charge_6_unit",
        "I.C 6 Rate - Value": "industry_charge_6_rate_value",
        "I.C 6 Rate - Unit": "industry_charge_6_rate_unit",
        "I.C 6 Charges": "industry_charge_6_charges",
        "Industry Charges 7 - Name": "industry_charge_7_name",
        "I.C 7 Quantity 1 - Value": "industry_charge_7_quantity_1_value",
        "I.C 7 Quantity 1 - Unit": "industry_charge_7_quantity_1_unit",
        "I.C 7 Quantity 2 - Value": "industry_charge_7_quantity_2_value",
        "I.C 7 Quantity 2 - Unit": "industry_charge_7_quantity_2_unit",
        "I.C 7 Unit": "industry_charge_7_unit",
        "I.C 7 Rate - Value": "industry_charge_7_rate_value",
        "I.C 7 Rate - Unit": "industry_charge_7_rate_unit",
        "I.C 7 Charges": "industry_charge_7_charges",
        "Total Industry Charges": "total_industry_charges",
        "Levy 1 - Name": "levy_name",
        "Levy 1 Quantity": "levy_quantity",
        "Levy 1 Unit": "levy_unit",
        "Levy 1 Rate - Value": "levy_rate_value",
        "Levy 1 Rate - Unit": "levy_rate_unit",
        "Levy 1 Total": "levy_total",
        "Total  Levies": "total_levies",
        "Total Excluding VAT": "total_no_vat",
        "Applicable VAT": "applicable_vat",
        "VAT Charged": "charged_vat",
        "Bill Amount": "bill_amount",
        "Previous Amount": "previous_balance",
        "Amount To Pay": "total_amount",
    }
)

INDUSTRY_CHARGES_MAPPING = {
    "capacity": "Availability/ Capacity",
    "daily_capacity": "Capacity Charge",
    "standing_charge": "Standing Charge",
    "excess_capacity_charge": "Availability Charge",
    "reactive_charge": "Reactive Charge",
    "mop_hh": "MOP HH.",
    "da_dc_hh": "DA/DC HH.",
    "distribution_charge": "Distribution Fixed Charge",
    "transmission_charge": "National Grid Transmission Fixed Charge",
}


def exclude_electricity_charges_fields(headers, template_column_mapping):
    template_column_names = [
        column_name.replace("`", "")
        for column_name in template_column_mapping.values()
    ]
    column_headers = deepcopy(headers)
    for header in [
        "Opening Reading",
        "Opening Reading Type",
        "Opening Reading Date",
        "Last Reading",
        "Last Reading Type",
        "Last Reading Date",
        "Consumption",
        "Rate",
        "Day Consumption - Value",
        "Day Consumption - Unit",
        "Day Rate - Value",
        "Day Rate - Unit",
        "Day Charges",
        "Night Consumption - Value",
        "Night Consumption - Unit",
        "Night Rate - Value",
        "Night Rate - Unit",
        "Night Charges",
    ]:
        if header not in template_column_names:
            column_headers.pop(header, None)
    return column_headers


def write_excel_row(
    ws: Worksheet, row_number: int, headers: list, data: dict
) -> None:
    for field, column_value in data.items():
        if isinstance(column_value, (list, dict)):
            continue

        try:
            column_number = headers.index(field) + 1
            ws.cell(row=row_number, column=column_number, value=column_value)
        except ValueError:
            continue


def get_mapped_json_data(mapped_data: dict, headers: list, data: dict) -> None:
    for field, column_value in data.items():
        if isinstance(column_value, (list, dict)):
            continue

        try:
            column_index = list(headers.values()).index(field)
            mapped_field = list(headers.keys())[column_index]
        except ValueError:
            continue

        if mapped_field.lower().endswith("date") or mapped_field.lower() in [
            "bill from",
            "bill to",
        ]:
            try:
                column_value = int(
                    datetime.fromisoformat(column_value).timestamp() * 1000
                )
            except ValueError:
                column_value = None

        mapped_data[mapped_field] = (
            column_value if column_value is not None else ""
        )

    return mapped_data


def get_electricity_charges(
    meter: BillingServiceMeter,
    meter_invoice: MeterInvoice,
    billing_service_contract: BillingServiceContract,
    customer_portal_customer_id: int,
) -> None:
    period_start_at = meter_invoice.data_file_request.period_start_at
    period_end_at = meter_invoice.data_file_request.period_end_at
    period_day_diff = (period_end_at - period_start_at).days

    try:
        data_service_meter = BillingServiceMeter.objects.get(
            electricity_customer_account__customer__customer_portal_id=customer_portal_customer_id,
            mpan__mpan=meter_invoice.customer_billing_details.mpan,
        )

        data_service_contract_meter = BillingServiceContractMeter.objects.get(
            contract=billing_service_contract, meter=data_service_meter
        )
    except (
        BillingServiceMeter.DoesNotExist,
        BillingServiceContractMeter.DoesNotExist,
    ):
        return

    night_time_start = (
        data_service_contract_meter.contract.night_time_start.isoformat()
    )
    night_time_end = (
        data_service_contract_meter.contract.night_time_end.isoformat()
    )

    meter_consumption_charges = meter.consumptions.filter(
        Q(
            created_at__date__gte=period_start_at,
            created_at__date__lte=period_end_at,
        )
    ).aggregate(
        day_consumption=Coalesce(
            Sum("consumption", filter=Q(created_at__time__gt=night_time_end)),
            0,
            output_field=DecimalField(),
        ),
        night_consumption=Coalesce(
            Sum(
                "consumption",
                filter=Q(
                    created_at__time__gte=night_time_start,
                    created_at__time__lte=night_time_end,
                ),
            ),
            0,
            output_field=DecimalField(),
        ),
        day_cost=Coalesce(
            Sum("cost", filter=Q(created_at__time__gt=night_time_end)),
            0,
            output_field=DecimalField(),
        ),
        night_cost=Coalesce(
            Sum(
                "cost",
                filter=Q(
                    created_at__time__gte=night_time_start,
                    created_at__time__lte=night_time_end,
                ),
            ),
            0,
            output_field=DecimalField(),
        ),
    )

    hh_consumption_charges = HHConsumptionCharges.objects.create(
        day_consumption_value=meter_consumption_charges["day_consumption"],
        day_rate_value=data_service_contract_meter.day_unit_rate,
        day_charges=meter_consumption_charges["day_cost"],
        night_consumption_value=meter_consumption_charges["night_consumption"],
        night_rate_value=data_service_contract_meter.night_unit_rate,
        night_charges=meter_consumption_charges["night_cost"],
        total_electricity_charges=(
            meter_consumption_charges["day_cost"]
            + meter_consumption_charges["night_cost"]
        ),
    )

    meter_invoice.hh_consumption_charges = hh_consumption_charges

    if meter.opening_reading and meter.last_reading:
        reading_consumption_charge = ReadingConsumptionCharges.objects.create(
            opening_reading=meter.opening_reading,
            opening_reading_date=meter.opening_reading_at.date(),
            last_reading=meter.last_reading,
            last_reading_date=meter.last_reading_at.date(),
            consumption=meter.last_reading - meter.opening_reading,
            total_electricity_charges=(
                (meter.last_reading - meter.opening_reading)
                / (
                    meter.last_reading_at.date()
                    - meter.opening_reading_at.date()
                ).days
            ),
        )

        meter_invoice.reading_consumption_charges = reading_consumption_charge

    industry_charges = []
    for field in BillingServiceContractMeter._meta.fields:
        if (
            INDUSTRY_CHARGES_MAPPING.get(field.name)
            and getattr(data_service_contract_meter, field.name) is not None
        ):
            if field.name in [
                "standing_charge",
                "daily_capacity",
                "distribution_charge",
                "transmission_charge",
            ]:
                rate_value = getattr(data_service_contract_meter, field.name)
                industry_charges.append(
                    IndustryCharges(
                        meter_invoice=meter_invoice,
                        name=INDUSTRY_CHARGES_MAPPING[field.name],
                        quantity_1_value=period_day_diff,
                        quantity_1_unit="days",
                        unit="Day",
                        rate_value=rate_value,
                        rate_unit="p/day",
                        charges=(rate_value * period_day_diff) / 100,
                    )
                )
            else:
                industry_charges.append(
                    IndustryCharges(
                        meter_invoice=meter_invoice,
                        name=INDUSTRY_CHARGES_MAPPING[field.name],
                        quantity_1_value=getattr(
                            data_service_contract_meter, field.name
                        ),
                        charges=getattr(
                            data_service_contract_meter, field.name
                        ),
                    )
                )
        elif field.name.endswith("_levy"):
            meter_invoice.levy_name = "Climate Change Levy"
            meter_invoice.levy_quantity = getattr(
                data_service_contract_meter, field.name
            )
            meter_invoice.levy_total = meter_invoice.levy_quantity
            meter_invoice.total_levies = meter_invoice.levy_quantity

    IndustryCharges.objects.bulk_create(industry_charges)
    meter_invoice.data_center_contract_meter_id = data_service_contract_meter.id
    meter_invoice.save()
