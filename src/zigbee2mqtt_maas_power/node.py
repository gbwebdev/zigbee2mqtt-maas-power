import json
import logging

from zigbee2mqtt_maas_power.mqtt import Mqtt

logger = logging.getLogger()

class Node:
    def __init__(self, node_conf, mqtt):
        self._mqtt = mqtt
        self._node_conf = node_conf
        self._set_state_topic = Mqtt().get_full_topic(node_conf.set_state_topic)
        self._read_state_topic = Mqtt().get_full_topic(node_conf.read_state_topic)
        self._read_state_payload_key = node_conf.read_state_payload_key
        self._invert = node_conf.pdu.invert
        self._pdu: None
        self._switch_id: None
        self._power_on_extra_probe: []
        self._power_state = None
        logger.debug("Registering listener to \"%s\"", self._read_state_topic)
        self._mqtt.register_state_listener(self._read_state_topic, self.on_read_state)

    @property
    def power_state(self):
        return self._power_state

    def power_on(self):
        # Publish a power on message
        state = "OFF" if self._invert else "ON"
        self._mqtt.publish(self._set_state_topic, state)

    def power_off(self):
        # Publish a power off message
        state = "ON" if self._invert else "OFF"
        self._mqtt.publish(self._set_state_topic, state)

    def on_read_state(self, payload):
        # Callback for when a new state is read on mqtt
        logger.info("Searching for %s in %s", self._read_state_payload_key, payload)
        payload = json.loads(payload)
        # Read the state from the payload
        if self._read_state_payload_key in payload:
            self._power_state = payload[self._read_state_payload_key]

