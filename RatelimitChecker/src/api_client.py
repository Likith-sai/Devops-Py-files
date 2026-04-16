import logging
import requests

logger = logging.getLogger(__name__)

def make_request(url: str) -> dict:
    try:
        response = requests.get(url)
        response_time = response.elapsed.total_seconds()
        return {
            "status_code": response.status_code,
            "response_time": response_time
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP Request failed: {e}")
        return None