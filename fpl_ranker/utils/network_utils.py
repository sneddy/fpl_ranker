import requests

requests.packages.urllib3.disable_warnings()

from tenacity import (Retrying, retry_if_exception_type, stop_after_attempt,
                      wait_fixed)


def safe_request(url, n_retry=50):
    exceptions = (requests.exceptions.Timeout, ValueError, requests.exceptions.SSLError)
    for attempt in Retrying(
            stop=stop_after_attempt(n_retry),
            wait=wait_fixed(10),
            retry=retry_if_exception_type(exceptions),
            reraise=True,
    ):
        with attempt:
            response = requests.get(url, verify=False)
            if response.status_code != 200:
                raise ValueError(f"Unexpected status code: {response.status_code} during {request_type}")
            return response.json()
