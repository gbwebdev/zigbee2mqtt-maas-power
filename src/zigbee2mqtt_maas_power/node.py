class Node:
    def __init__(self, node_conf, mqtt):
        self._mqtt = mqtt
        self._node_conf = node_conf
        self._set_state_topic = node_conf.set_state_topic
        self._read_state_topic = node_conf.read_state_topic
        self._read_state_payload_key = node_conf.read_state_payload_key
        self._invert = node_conf.pdu.invert
        self._pdu: None
        self._switch_id: None
        self._power_on_extra_probe: []
        self._power_state = None
        
        self._mqtt.register_state_listener(self._read_state_topic, self.on_read_state)

    def power_on(self):
        # Publish a power on message
        self._mqtt.publish(self._set_state_topic, "OFF" if self._invert else "ON")

    def power_off(self):
        # Publish a power off message
        self._mqtt.publish(self._set_state_topic, "ON" if self._invert else "OFF")

    def get_power_state(self):
        # Publish a power off message
        self._mqtt.publish(self._set_state_topic, "ON" if self._invert else "OFF")
    
    def on_read_state(self, payload):
        # Read the state from the payload
        if self._read_state_payload_key in payload:
            self._power_state = payload[self._read_state_payload_key]

