from collections import OrderedDict
from copy import deepcopy
from datetime import datetime

from invoices.models import (
    HHConsumptionCharges,
    IndustryCharges,
    MeterInvoice,
    ReadingConsumptionCharges,
)
from openpyxl.worksheet.worksheet import Worksheet
from sources.data_service.models import (
    DataServiceContract,
    DataServiceContractMeter,
    DataServiceMeter,
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
    "capacity": "Availability/ Capacity",  # TODO: confirm if correct mapping
    "standing_charge": "Standing Charge",
    "excess_capacity_charge": "Excess Capacity Charge",
    "reactive_charge": "Reactive Charge",
    "transmission_charge": "Transmission Charges",
    "mop_hh": "MOP HH.",
    "da_dc_hh": "DA/DC HH.",
}


def exclude_electricity_charges_fields(headers, electricity_charge="hh"):
    column_headers = deepcopy(headers)
    if electricity_charge == "hh":
        for header in [
            "Opening Reading",
            "Opening Reading Type",
            "Opening Reading Date",
            "Last Reading",
            "Last Reading Type",
            "Last Reading Date",
            "Consumption",
            "Rate",
        ]:
            column_headers.pop(header, None)
    elif electricity_charge == "readings":
        for header in [
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
    meter: DataServiceMeter,
    meter_invoice: MeterInvoice,
    data_service_contract: DataServiceContract,
    customer_portal_customer_id: int,
) -> None:
    try:
        data_service_meter = DataServiceMeter.objects.get(
            customer__customer_portal_id=customer_portal_customer_id,
            mpan__mpan=meter_invoice.customer_billing_details.mpan,
        )

        data_service_contract_meter = DataServiceContractMeter.objects.get(
            contract=data_service_contract, meter=data_service_meter
        )
    except (
        DataServiceMeter.DoesNotExist,
        DataServiceContractMeter.DoesNotExist,
    ):
        return

    hh_consumption_charges = HHConsumptionCharges.objects.create(
        day_consumption_value=meter.day_consumption,
        day_rate_value=data_service_contract_meter.day_unit_rate,
        day_charges=meter.day_cost,
        night_consumption_value=meter.night_consumption,
        night_rate_value=data_service_contract_meter.night_unit_rate,
        night_charges=meter.night_cost,
        total_electricity_charges=(
            (meter.day_cost or 0) + (meter.night_cost or 0)
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
    for field in DataServiceContractMeter._meta.fields:
        if (
            INDUSTRY_CHARGES_MAPPING.get(field.name)
            and getattr(data_service_contract_meter, field.name) is not None
        ):
            industry_charges.append(
                IndustryCharges(
                    meter_invoice=meter_invoice,
                    name=INDUSTRY_CHARGES_MAPPING[field.name],
                    quantity_1_value=getattr(
                        data_service_contract_meter, field.name
                    ),
                    # TODO: this still needs to change once unit in
                    #       industry charges is added
                    charges=getattr(data_service_contract_meter, field.name),
                )
            )
        elif field.name.endswith("_levy"):
            meter_invoice.levy_name = "Climate Change Levy"
            meter_invoice.levy_quantity = getattr(
                data_service_contract_meter, field.name
            )
            # TODO: this still needs to change once unit in levy is added
            meter_invoice.levy_total = meter_invoice.levy_quantity
            meter_invoice.total_levies = meter_invoice.levy_quantity

    IndustryCharges.objects.bulk_create(industry_charges)
    meter_invoice.data_center_contract_meter_id = data_service_contract_meter.id
    meter_invoice.save()
