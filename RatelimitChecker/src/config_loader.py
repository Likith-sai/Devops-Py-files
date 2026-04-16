import logging
import yaml

logger = logging.getLogger(__name__)


def load_config(config_path:str)-> dict:
    #print(type(config_path))
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"Configuration loaded successfully from {config_path}")
            return config
    except FileNotFoundError:
        logger.error(f"Error: Configuration file not found at {config_path}")
        return None
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        return None