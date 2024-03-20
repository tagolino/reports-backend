import json
from datetime import datetime
from io import BytesIO

import pandas
from templates.jmespath import search

minimum_timestamp = datetime(2000, 1, 1).timestamp()


def parse_value(value):
    if isinstance(value, str):
        try:
            date = datetime.strptime(value, "%d/%m/%Y").date()
            timestamp = int(date.timestamp())

            if timestamp >= minimum_timestamp:
                return timestamp * 1000
        except Exception:
            return value

    if isinstance(value, pandas.Timestamp):
        return int(value.timestamp() * 1000)

    if isinstance(value, int):
        return str(value)

    return value


def custom_converter(value):
    if pandas.isnull(value):
        return None

    return parse_value(value)


def get_file_json_content(uploaded_file):
    file_content = uploaded_file.read()
    file_extension = uploaded_file.name.split(".")[-1].lower()

    if file_extension == "json":
        json_content = file_content.decode("utf-8")
    elif file_extension == "xlsx":
        json_content = (
            pandas.read_excel(BytesIO(file_content), dtype=object)
            .map(custom_converter)
            .to_json(orient="records")
        )

    return json.loads(json_content)


def map_data(json_data, mapping_expression):
    if not mapping_expression:
        return json_data

    mapped_data = {}

    for key, value in mapping_expression.items():
        mapped_value = "ERROR"

        try:
            mapped_value = search(value.replace("`", '"'), json_data)
        except Exception as e:
            print(e)

        mapped_data[key] = mapped_value

    return mapped_data
