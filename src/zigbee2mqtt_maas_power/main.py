import argparse
import os
import sys

from flask import Flask, g, jsonify

from zigbee2mqtt_maas_power import configure_logger
from zigbee2mqtt_maas_power.config import Config
from zigbee2mqtt_maas_power.mqtt import Mqtt
from zigbee2mqtt_maas_power.node import Node
from zigbee2mqtt_maas_power.routes import register_routes

def create_app(args = None):
    """
    Factory function to create and configure the Flask app.
    """

    config = Config()
    config.load(args)

    if args:
        log_level = args.log_level
    else:
        log_level = os.getenv("ZMP_LOG_LEVEL", "INFO")
    
    app = Flask(__name__)
    
    app.logger = configure_logger(log_level)

    mqtt = Mqtt(config.mqtt)

    nodes = {}

    for node_name, node_conf in config.nodes.items():
        node = Node(node_conf, mqtt)
        nodes[node_name] = node

    # Store shared objects in app context
    app.config["config"] = config
    app.config["mqtt"] = mqtt
    app.config["nodes"] = nodes

    register_routes(app)

    return app

def cli():
    """
    Entry point for CLI usage (defined in pyproject.toml).
    """
    parser = argparse.ArgumentParser(description="zigbee2mqtt-maas-power CLI")

    # CLI arguments
    parser.add_argument("--config", type=str, help="Path to config file (YAML)", default=None)
    parser.add_argument("--log-level", type=str, help="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)", default=None)
    parser.add_argument("--mqtt-server", type=str, help="MQTT server URL", default=None)
    parser.add_argument("--mqtt-port", type=int, help="MQTT server port", default=None)
    parser.add_argument("--mqtt-connect-timeout", type=int, help="MQTT connection timeout", default=None)
    parser.add_argument("--mqtt-base-topic", type=str, help="MQTT base topic for zigbee messages", default=None)
    parser.add_argument("--mqtt-tls", type=bool, help="Enable TLS for MQTT", default=None)
    parser.add_argument("--mqtt-ca-cert", type=str, help="Path to MQTT's CA certificate", default=None)
    parser.add_argument("--mqtt-client-cert", type=str, help="MQTT certificate for client authentication", default=None)
    parser.add_argument("--mqtt-client-key", type=str, help="MQTT key for client authentication", default=None)
    parser.add_argument("--mqtt-username", type=str, help="MQTT username", default=None)
    parser.add_argument("--mqtt-password", type=str, help="MQTT password", default=None)
    parser.add_argument("--http-server-address", type=str, help="Address to bind http server to", default=None)
    parser.add_argument("--http-server-port", type=str, help="Port to bind http server to", default=None)
    parser.add_argument("--http-server-debug", type=bool, help="Run the seerver in debug mode", default=None)

    args = parser.parse_args()


    app = create_app(args)
    host=app.config["config"].http_server.server
    port=app.config["config"].http_server.port
    debug=app.config["config"].http_server.debug
    app.run(host=host, port=port, debug=debug)

    # Stop MQTT loop on exit
    app.config["mqtt"]._client.loop_stop()
    
    sys.exit(0)

if __name__ == "__main__":
    cli()
