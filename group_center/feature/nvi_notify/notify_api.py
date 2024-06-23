import requests

url: str = "http://localhost:8080"


def send_to_nvi_notify(dict_data: dict) -> bool:
    response = requests.post(url, data=dict_data)

    return response.status_code == 200
