import json
import logging


def load_json(config_path):
    try:
        with open(config_path, 'r') as json_file:
            config = json.load(json_file)
            return config
    except FileNotFoundError:
        logging.error(f"Json File not found: {config_path}")
        return None
    
def setup_logger():
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="logs/app.log"
    )    
