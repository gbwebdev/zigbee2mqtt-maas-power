# zigbee2mqtt-maas-power

A REST-to-MQTT gateway to manage servers' power from Canonical MAAS using Zigbee2MQTT.

## Using Docker

### Building

Simply run :
```console
$ docker image build -t gbwebdev/zigbee2mqtt-maas-power:$(cat .version) .
```
In the repo's root directory.

### Using

Edit the sample configuration file to match your setup and simply run :
```console
$ docker run \
    -v ./config.yaml:/etc/zigbee2mqtt_maas_power/config.yaml:ro \
    -p 5000:5000 \
    gbwebdev/zigbee2mqtt-maas-power
```


If you use a specific CA certificate and/or mTLS, you should mount them in the container.

For instance :
```console
$ ls ./ssl
ca.crt  mqtt_client.crt  mqtt_client.key
$ docker run \
    -v ./config.yaml:/etc/zigbee2mqtt_maas_power/config.yaml:ro \
    -v ./ssl:/etc/zigbee2mqtt_maas_power/ssl:ro \
    -p 5000:5000 \
    gbwebdev/zigbee2mqtt-maas-power
```

## Regular install

#TODO