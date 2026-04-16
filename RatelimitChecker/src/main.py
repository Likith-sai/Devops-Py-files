import argparse
import sys
import time
import logging
from config_loader import load_config
from api_client import make_request
from metrics import calculate_metrics
from transformer import suggest_rate_limit

def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s",
                        filename="app.log",
                        filemode="a")
    parser = argparse.ArgumentParser(
        description="Loads the configuration file and starts the application"
    )
    parser.add_argument("--config", "-c", required=True, help="Path to the configuration file")
    args = parser.parse_args()
    config = load_config(args.config)
    if config is None:
        logging.error("Failed to load configuration file.")
        sys.exit(1)
    url = config["api"]["url"]
    if url is None:
        logging.error("API URL not found in configuration.")
        sys.exit(1)
    else:
       total_requests = config["load"]["total_requests"]
       request_results = []
       for i in range(total_requests):
            response = make_request(url)
            time.sleep(3)
            request_results.append(response)
    calculations = calculate_metrics(request_results)
    rate_limit = suggest_rate_limit(calculations, config)
    logging.info(f"System Status: {rate_limit.system_status}")
    logging.info(f"Reason : {rate_limit.reason}")
    logging.info(f"Suggested rate limit: {rate_limit.suggested_rate_limit} requests per minute")

if __name__ == "__main__":
    main()