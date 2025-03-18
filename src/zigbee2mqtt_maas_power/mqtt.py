class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

import os
import paho.mqtt.client as mqtt
import ssl

from zigbee2mqtt_maas_power.config import Config

class Mqtt(metaclass=Singleton):
    
    def __init__(self, config: Config.Mqtt):
        self._client = mqtt.Client()
        self._client.on_publish = self.on_publish
        self._base_topic = config.base_topic

        self._handle_tls(config)
        self._handle_auth(config)
        self._client.connect(config.server, config.port)
        self._client.loop_start()
        
        
    
    def _handle_tls(self, config: Config.Mqtt):
        ca_cert = config.ca_cert
        cert = config.cert
        key = config.key
        if os.path.isfile(ca_cert):
            if os.path.isfile(cert) and os.path.isfile(key):
                self._client.tls_set(ca_cert, cert, key, ssl.CERT_REQUIRED, ssl.PROTOCOL_TLSv1_2)
            else:
                self._client.tls_set(ca_cert, ssl.PROTOCOL_TLSv1_2)
        #self._client.tls_insecure_set(False)

    def _handle_auth(self, config: Config.Mqtt):
        if config.username and config.password:
            self._client.username_pw_set(config.username, config.password)

    def publish(self, topic, payload, qos=0, retain=False):
        topic = f"{self._base_topic}/{topic}"
        topic = topic.replace("//", "/")
        try:
            pub_res = self._client.publish(topic, payload, qos, retain)
            pub_res.wait_for_publish()
        except Exception as e:
            print(e)
            return False
        return True


    def on_publish(self, client, userdata, mid,  reason_code=None, properties=None):
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
        except Exception as e:
            print(e)
        try:
            print(userdata)
            print(reason_code)
        except Exception as e:
            print(e)
    
    def register_state_listener(self, topic, callback):
        self._client.message_callback_add(topic, callback)
        self._client.subscribe(topic)