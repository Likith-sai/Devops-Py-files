import logging
import subprocess
import requests

def check_server(server, timeout):
    try:
        if server["type"] == "ping":
            ping_result = subprocess.run(
                ["ping", "-c", "1", server["target"]],
                stdout = subprocess.DEVNULL
            )
            return ping_result.returncode == 0
        elif server["type"] == "http":
            http_result = requests.get(
                server["target"],
                timeout = server["timeout"]
            )
            return http_result.status_code == 200
    except Exception as e:
        logging.error(f"Error Checking {server['name']} {server['type']} : {e}")
        return False



