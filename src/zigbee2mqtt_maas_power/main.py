import argparse
import sys


import os
import yaml

from zigbee2mqtt_maas_power.config import Config


def main():
    """
    Entry point for CLI usage (defined in pyproject.toml).
    """
    parser = argparse.ArgumentParser(description="zigbee2mqtt-maas-power CLI")

    # CLI arguments
    parser.add_argument("--config", type=str, help="Path to config file (YAML)", default=None)
    parser.add_argument("--mqtt-ca-cert", type=str, help="Path to MQTT's CA certificate", default=None)
    parser.add_argument("--mqtt-server", type=str, help="MQTT server URL", default=None)
    parser.add_argument("--mqtt-username", type=str, help="MQTT username", default=None)
    parser.add_argument("--mqtt-password", type=str, help="MQTT password", default=None)
    parser.add_argument("--mqtt-cert", type=str, help="MQTT certificate for client authentication", default=None)
    parser.add_argument("--mqtt-key", type=str, help="MQTT key for client authentication", default=None)

    args = parser.parse_args()

    config = Config()
    config.load(args)

    print("Running")
    print(config.mqtt.server)
    # Return exit code 0 for success
    sys.exit(0)

if __name__ == "__main__":
    main()
