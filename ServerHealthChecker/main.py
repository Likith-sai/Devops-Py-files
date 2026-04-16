from utils import load_json, setup_logger
from checkers import check_server
import logging

class HealthCheck:
    def __init__(self, config):
        self.config = config
        self.results = []

    def run_checks(self):
        for server in self.config["servers"]:
            status = check_server(server, self.config["timeout"])
            self.results.append((server["name"], status))
            if status:
                logging.info(f"{server['name']} is healthy.")
            else:
                logging.warning(f"{server['name']} is unhealthy.")

    def generate_report(self):
        report = "Health Check Report:\n"
        up = sum(1 for _, status in self.results if status)
        down = len(self.results) - up
        report += f"Total Servers: {len(self.results)}\n"
        report += f"Healthy_servers: {up}\n"
        report += f"Unhealthy_servers: {down}\n"

        #print(report)
        logging.info(report)




if __name__ == "__main__":
    setup_logger()
    config = load_json("config.json")
    if not config:
        logging.error("Failed to load configuration. Exiting.")
        exit(1)

    checks = HealthCheck(config)
    checks.run_checks()
    checks.generate_report()