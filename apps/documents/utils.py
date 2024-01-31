import json

import pandas


def get_file_json_content(uploaded_file):
    file_content = uploaded_file.read()
    file_extension = uploaded_file.name.split(".")[-1].lower()

    if file_extension == "json":
        json_content = file_content.decode("utf-8")
    elif file_extension == "xlsx":
        json_content = pandas.read_excel(file_content).to_json(
            orient="records"
        )

    return json.loads(json_content)
