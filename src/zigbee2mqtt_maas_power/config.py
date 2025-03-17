class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

import yaml
import os
from jinja2 import nativetypes

class Config(metaclass=Singleton):
    # Define the configuration properties

    class Mqtt:
        # Define the MQTT configuration properties

        def __init__(self, config: dict, args):
            # Set default values for MQTT configuration properties then load the configuration
            self._server = "mqtt://localhost"
            self._port = 1883
            self._base_topic = "zigbee2mqtt"
            self._ca_cert = "/etc/zigbee2mqtt_maas_power/ssl/ca.crt"
            self._username = None
            self._password = None
            self._cert = "/etc/zigbee2mqtt_maas_power/ssl/client.crt"
            self._key = "/etc/zigbee2mqtt_maas_power/ssl/client.key"

            self._load(config, args)

        def _load(self, config: dict, args):
            # Load the MQTT configuration in the following order:
            # 1. Command line arguments
            # 2. Environment variables
            # 3. Configuration file
            # 4. Default values

            if args.mqtt_server:
                self._server = args.mqtt_server
            else:
                self._server = os.environ.get('ZMP_MQTT_SERVER',
                                              config.get('server',
                                                          self._server))
            if args.mqtt_port:
                self._port = args.mqtt_port
            else:
                self._port = os.environ.get('ZMP_MQTT_PORT',
                                            config.get('port',
                                                          self._port))
            if args.mqtt_base_topic:
                self._base_topic = args.mqtt_base_topic
            else:
                self._base_topic = os.environ.get('ZMP_MQTT_BASE_TOPIC',
                                                  config.get('base_topic',
                                                             self._base_topic))

            if args.mqtt_ca_cert:
                self._ca_cert = args.mqtt_ca_cert
            else:
                self._ca_cert = os.environ.get('ZMP_MQTT_CA_CERT',
                                               config.get('ca_cert',
                                                          self._ca_cert))
            if args.mqtt_username:
                self._username = args.mqtt_username
            else:
                self._username = os.environ.get('ZMP_MQTT_USERNAME',
                                                 config.get('username',
                                                            self._username))
            if args.mqtt_password:
                self._password = args.mqtt_password
            else:
                self._password = os.environ.get('ZMP_MQTT_PASSWORD',
                                                 config.get('password',
                                                            self._password))
            if args.mqtt_cert:
                self._cert = args.mqtt_cert
            else:
                self._cert = os.environ.get('ZMP_MQTT_CERT',
                                            config.get('cert',
                                                       self._cert))
            if args.mqtt_key:
                self._key = args.mqtt_key
            else:
                self._key = os.environ.get('ZMP_MQTT_KEY',
                                           config.get('key',
                                                      self._key))

        @property
        def base_topic(self):
            # Return the base topic
            return self._base_topic

        @property
        def server(self):
            # Return the MQTT server URL
            return self._server

        @property
        def port(self):
            # Return the MQTT server port
            return self._port
        
        @property
        def ca_cert(self):
            # Return the CA certificate path
            return self._ca_cert
        
        @property
        def username(self):
            # Return the MQTT username
            return self._username
        
        @property
        def password(self):
            # Return the MQTT password
            return self._password
        
        @property
        def cert(self):
            # Return the client certificate
            return self._cert
        
        @property
        def key(self):
            # Return the client key
            return self._key
        
    class Pdu:
        # Define the PDU configuration properties

        def __init__(self):
            # Set default values for PDU configuration properties
            self._invert = False
            self._set_state_topic = None
            self._read_state_topic = None
            self._read_state_payload_key = None

        def load(self, config: dict):
            # Load the PDU configuration

            self._invert = config.get('invert', self._invert)
            self._set_state_topic = config.get('set_state_topic')
            self._read_state_topic = config.get('read_state_topic')
            self._read_state_payload_key = config.get('read_state_payload_key')

        @property
        def invert(self):
            # Return the invert property
            return self._invert

        @property
        def set_state_topic(self):
            # Return the set state topic
            return self._set_state_topic

        @property
        def read_state_topic(self):
            # Return the read state topic
            return self._read_state_topic

        @property
        def read_state_payload_key(self):
            # Return the read state payload key
            return self._read_state_payload_key

    class Node:

        def __init__(self):
            self._pdu: None
            self._switch_id: None
            self._power_on_extra_probe: []

        @property
        def pdu(self):
            return self._pdu

        @property
        def switch_id(self):
            return self._switch_id

        @property
        def power_on_extra_probe(self):
            return self._power_on_extra_probe

        @property
        def set_state_topic(self):
            return nativetypes.NativeEnvironment() \
                    .from_string(self._pdu.set_state_topic) \
                    .render(switch_id=self._switch_id)

        @property
        def read_state_topic(self):
            return nativetypes.NativeEnvironment() \
                    .from_string(self._pdu.read_state_topic) \
                    .render(switch_id=self._switch_id)
        
        @property
        def read_state_payload_key(self):
            return nativetypes.NativeEnvironment() \
                    .from_string(self._pdu.read_state_payload_key) \
                    .render(switch_id=self._switch_id)
        
        def load(self, config, pdus):
            self._pdu = pdus.get(config.get('pdu'))
            self._switch_id = config.get('switch_id')
            self._power_on_extra_probe = config.get('power_on_extra_probe', [])

    def __init__(self):
        self._conf_file_path = '/etc/zigbee2mqtt_maas_power/config.yaml'
        self.mqtt = None
        self.pdus = {}
        self.nodes = {}

    def load(self, args):
        # Load the configuration in the following order:
        # 1. Command line arguments
        # 2. Environment variables
        # 3. Configuration file
        # 4. Default values
        
        if args.config:
            self._conf_file_path = args.config
        else:
            self._conf_file_path = os.environ.get('ZMP_CONF_FILE',
                                                  self._conf_file_path)

        # Load the configuration file
        try:
            with open(self._conf_file_path,
                      'r',
                      encoding="utf-8") as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            config = {}

        # Load the MQTT configuration
        self.mqtt = self.Mqtt(config.get("mqtt", {}), args)
        
        self._load_pdus(config.get("pdus", {}))
        self._load_nodes(config.get("nodes", {}))

    def _load_pdus(self, config):
        for pdu_id, pdu_conf in config.items():
            pdu = self.Pdu()
            pdu.load(pdu_conf)
            self.pdus[pdu_id] = pdu

    def _load_nodes(self, config):
        for node_id, node_conf in config.items():
            node = self.Node()
            node.load(node_conf, self.pdus)
            self.nodes[node_id] = node
