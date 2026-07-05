import requests

REQUEST_TIMEOUT = 20

def api_get(base_url: str, path: str, params: dict | None):
    response = requests.get(
        f"{base_url.rstrip("/")}{path}",
        params = params,
        timeout = REQUEST_TIMEOUT
    )

    response.raise_for_status()
    return response.json()