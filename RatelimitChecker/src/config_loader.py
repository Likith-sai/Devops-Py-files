from flask import logging
import yaml

def load_config(config_path: str)-> dict:
    #print(type(config_path))
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            logging.info(f"Configuration loaded successfully from {config_path}")
            return config
    except FileNotFoundError:
        logging.error(f"Error: Configuration file not found at {config_path}")
        return None
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML file: {e}")
        return None