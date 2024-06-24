import requests

url: str = "http://localhost:8080"


def get_nvi_notify_api_url(target: str):
    return url.strip() + target.strip()


def send_to_nvi_notify(dict_data: dict, target: str) -> bool:
    response = requests.post(get_nvi_notify_api_url(target), data=dict_data)

    return response.status_code == 200
