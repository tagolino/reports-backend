import json
from io import BytesIO

import pandas
from templates.jmespath import search


def custom_converter(value):
    if pandas.isnull(value):
        return None

    return str(value)


def get_file_json_content(uploaded_file):
    file_content = uploaded_file.read()
    file_extension = uploaded_file.name.split(".")[-1].lower()

    if file_extension == "json":
        json_content = file_content.decode("utf-8")
    elif file_extension == "xlsx":
        data = pandas.read_excel(BytesIO(file_content), parse_dates=True)
        content = data.map(custom_converter)
        json_content = content.to_json(orient="records")

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
