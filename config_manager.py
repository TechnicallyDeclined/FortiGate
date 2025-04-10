import yaml

def load_config(config_file="config.yaml"):
    """Loads configuration data from a YAML file."""
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML format in '{config_file}': {e}")
        return None

# You could also have functions here to manage the configuration data directly
# if you don't want to load from a file.