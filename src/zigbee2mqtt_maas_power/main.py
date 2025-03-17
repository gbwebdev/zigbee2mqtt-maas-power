import argparse
import sys

from zigbee2mqtt_maas_power.config import Config
from zigbee2mqtt_maas_power.mqtt import Mqtt

def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !")

def main():
    """
    Entry point for CLI usage (defined in pyproject.toml).
    """
    parser = argparse.ArgumentParser(description="zigbee2mqtt-maas-power CLI")

    # CLI arguments
    parser.add_argument("--config", type=str, help="Path to config file (YAML)", default=None)
    parser.add_argument("--mqtt-port", type=int, help="MQTT server port", default=None)
    parser.add_argument("--mqtt-server", type=str, help="MQTT server URL", default=None)
    parser.add_argument("--mqtt-base-topic", type=str, help="MQTT base topic for zigbee messages", default=None)
    parser.add_argument("--mqtt-ca-cert", type=str, help="Path to MQTT's CA certificate", default=None)
    parser.add_argument("--mqtt-username", type=str, help="MQTT username", default=None)
    parser.add_argument("--mqtt-password", type=str, help="MQTT password", default=None)
    parser.add_argument("--mqtt-cert", type=str, help="MQTT certificate for client authentication", default=None)
    parser.add_argument("--mqtt-key", type=str, help="MQTT key for client authentication", default=None)

    args = parser.parse_args()

    config = Config()
    config.load(args)

    print("Running")
    print(config.mqtt.server)

    for node_name, node_conf in config.nodes.items():
        print(node_name)
        print(node_conf.set_state_topic)
        print(node_conf.read_state_topic)
        print(node_conf.read_state_payload_key)


    # Create the MQTT client
    mqtt = Mqtt(config.mqtt)

    mqtt.publish("test", "Hello, world!")

    # Return exit code 0 for success
    sys.exit(0)

if __name__ == "__main__":
    main()
