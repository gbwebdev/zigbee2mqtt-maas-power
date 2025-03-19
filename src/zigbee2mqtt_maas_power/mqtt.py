class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

import os
import time
import paho.mqtt.client as mqtt
import ssl

from zigbee2mqtt_maas_power.config import Config

class Mqtt(metaclass=Singleton):
    
    def __init__(self, config: Config.Mqtt):
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_connect_fail = self._on_connect_fail
        self._client.on_publish = self._on_publish

        self._base_topic = config.base_topic
        self._topic_listeners = {}

        self._handle_tls(config)
        self._handle_auth(config)
        self._client.connect(config.server, config.port)
        self._client.loop_start()

        for i in range(config.connect_timeout*4):
            time.sleep(0.25)
            if self._client.is_connected():
                break

        if not self._client.is_connected():
            print("Failed to connect to MQTT broker")
            exit(1)
                                     
        
    
    def _handle_tls(self, config: Config.Mqtt):
        if config.tls:
            print("TLS enabled for MQTT")
            ca_cert = config.ca_cert
            cert = config.client_cert
            key = config.client_key
            if os.path.isfile(ca_cert):
                print("Found CA certificate")
                if os.path.isfile(cert) and os.path.isfile(key):
                    print("Found client certificate and key : will continue with mtls authentication")
                    self._client.tls_set(ca_cert, cert, key, ssl.CERT_REQUIRED, ssl.PROTOCOL_TLSv1_2)
                else:
                    print("Client certificate and key not found, will try simple TLS connection (no mtls)")
                    self._client.tls_set(ca_cert, ssl.PROTOCOL_TLSv1_2)
            else:
                print("No CA certificate found, will try with system's CA certificates")
                self._client.tls_set()
        else:
            print("TLS disabled for MQTT")

    def _handle_auth(self, config: Config.Mqtt):
        if config.username and config.password:
            print("Username and password specified for MQTT, using password authentication")
            self._client.username_pw_set(config.username, config.password)
        else:
            print("No username and password specified for MQTT, will try without password authentication")

    def publish(self, topic, payload, qos=0, retain=False):
        print(f"Publishing to {topic}: {payload}")
        try:
            pub_res = self._client.publish(topic, payload, qos, retain)
            pub_res.wait_for_publish()
        except Exception as e:
            print(e)
            return False
        return True

    def _on_publish(self, client, userdata, mid,  reason_code=None, properties=None):
        # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
        try:
            userdata.remove(mid)
        except KeyError:
            print("on_publish() is called with a mid not present in unacked_publish")
        except Exception as e:
            print(e)
    
    def _on_connect(client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
    
    def _on_connect_fail(client, userdata, flags, reason_code, properties):
        print(f"Connection failed with result code {reason_code}")
        exit(1)

    def register_state_listener(self, topic, callback):
        if topic in self._topic_listeners:
            self._topic_listeners[topic].append(callback)
        else:
            self._topic_listeners[topic] = [callback]
            self._client.message_callback_add(topic, self._dispatch_message)
            self._client.subscribe(topic)
    
    def _dispatch_message(self, client, userdata, message):
        for listener in self._topic_listeners.get(message.topic, []):
            listener(message.payload)
    
    def get_full_topic(self, topic):
        if topic.startswith(f"{self._base_topic}"):
            return topic
        else:
            return f"{self._base_topic}/{topic}"