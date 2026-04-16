from flask import logging
import requests

def make_request(url: str) -> dict:
    try:
        response = requests.get(url)
        response_time = response.elapsed.total_seconds()
        return {
            "status_code": response.status_code,
            "response_time": response_time
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP Request failed: {e}")
        return None