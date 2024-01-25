import requests
from django.conf import settings
from urllib.parse import urljoin

CARBONE_IO_API_URL = settings.CARBONE_IO_API_URL
CARBONE_IO_API_TEST_TOKEN = settings.CARBONE_IO_API_TEST_TOKEN


def get_authentication_headers(api_token):
    return {
        'Authorization': 'Bearer ' + api_token,
        'carbone-version': '4'
    }


def add_template(template_file):
    endpoint_url = urljoin(CARBONE_IO_API_URL, "/template")

    try:
        form_data = {
            'template': (template_file.name, template_file.read(), template_file.content_type)
        }
        headers = {
            **get_authentication_headers(CARBONE_IO_API_TEST_TOKEN),
        }

        response = requests.post(
            endpoint_url, files=form_data, headers=headers)

        return response.json()
    except Exception as e:
        print(f"Error uploading template: {e}")

        return None
