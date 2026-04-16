import yaml

def load_config(config_path):
    #print(type(config_path))
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            print(f"Configuration loaded successfully from {config_path}")
            return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None