import os
import argparse
import yaml
import sys

def load_config_from_file(file_path):
    """
    Load settings from a YAML file.
    """
    with open(file_path, 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    """
    Entry point for CLI usage (defined in pyproject.toml).
    """
    parser = argparse.ArgumentParser(description="zigbee2mqtt-maas-power CLI")

    # CLI arguments
    parser.add_argument("--config", type=str, help="Path to config file (YAML)", default="/etc/zigbee2mqtt_maas_power.yaml")
    # parser.add_argument("--option", type=str, help="An example option from CLI", default=None)

    args = parser.parse_args()

    # 1. Load config if provided
    config = {}
    if args.config:
        try:
            config = load_config_from_file(args.config)
        except FileNotFoundError:
            print(f"Config file {args.config} not found.", file=sys.stderr)
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML config: {e}", file=sys.stderr)
            sys.exit(1)

    # 2. Environment variables override or provide defaults if not in config
    # env_option = os.environ.get("MY_PACKAGE_OPTION")

    # 3. Command line arguments can override both environment and config
    # final_option = args.option or env_option or config.get("option", "default_value")

    # Use final_option for your app logic
    # print(f"Running with option = {final_option}")
    print("Running")
    # Return exit code 0 for success
    sys.exit(0)

if __name__ == "__main__":
    main()
