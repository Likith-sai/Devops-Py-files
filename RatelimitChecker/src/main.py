import argparse
import sys
from config_loader import load_config
from api_client import make_request
from metrics import calculate_metrics
from transformer import suggest_rate_limit

def main():
    parser = argparse.ArgumentParser(
        description="Loads the configuration file and starts the application"
    )
    parser.add_argument("--config", "-c", required=True, help="Path to the configuration file")
    args = parser.parse_args()
    config = load_config(args.config)
    if config is None:
        print("Failed to load configuration file.")
        sys.exit(1)
    url = config["api"]["url"]
    if url is None:
        print("API URL not found in configuration.")
        exit(1)
    else:
       total_requests = config["load"]["total_requests"]
       request_results = []
       for i in range(total_requests):
        response = make_request(url)
        request_results.append(response)
    calculations = calculate_metrics(request_results)
    rate_limit = suggest_rate_limit(calculations, config)
    print(f"System Status: {rate_limit.get("system_status")}")
    print(f"Reason : {rate_limit.get("reason")}")
    print(f"Suggested rate limit: {rate_limit.get('suggested_rate_limit')} requests per minute")

if __name__ == "__main__":
    main()