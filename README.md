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
    -p 5083:80 \
    gbwebdev/zigbee2mqtt-maas-power
```
or, using `docker compose`:
```console
$ docker compose up
```

If you use a specific CA certificate and/or mTLS, you should mount them in the container.

For instance :
```console
$ ls ./ssl
ca.crt  mqtt_client.crt  mqtt_client.key
$ docker run \
    -v ./config.yaml:/etc/zigbee2mqtt_maas_power/config.yaml:ro \
    -v ./ssl:/etc/zigbee2mqtt_maas_power/ssl:ro \
    -p 5083:80 \
    gbwebdev/zigbee2mqtt-maas-power
```
(you can uncomment the corresponding line in the docker-compose file).

## Regular install

### Installing

Simply run :
```console
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install .
```
In the repo's root directory.

### Using

#### Production

Edit the sample configuration file to match your setup and simply run :
```console
$ export ZMP_CONF_FILE=$(pwd)/config.yaml
$ gunicorn -w 1 zigbee2mqtt_maas_power.wsgi:app
```

#### Dev/Test

Edit the sample configuration file to match your setup and simply run :
```console
$ zmp
```

## Configuration

You absolutly need a configuration file to define PDUs and Nodes.

The program will look for a configuration file at `etc/zigbee2mqtt_maas_power/config.yaml` and will fallback on `./config.yaml`. \
You can also set a different configuration file path using the environment variable `ZMP_CONF_FILE` or the argument `--config` in CLI mode.

For HTTP and MQTT configuration, you can use the configuration file, but you can also override the settings using environment variables, and/or CLI arguments :
- CLI arguments when using `zmp`
  Run `zmp --help` for a complete list
- Environment variables :
  | **Variable**             | **Definition**                                                                                      | **Default value**                                                                                                     |
  |--------------------------|-----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
  | ZMP_CONF_FILE            | Configuration file path                                                                             | `/etc/zigbee2mqtt_maas_power/config.yaml` (fallback on `./config.yaml`)      
  | ZMP_LOG_LEVEL            | Log level                                           | `INFO`                                              |
  | ZMP_HTTP_SERVER_ADDRESS  | Flask's http server address (not used by wsgi server)                                               | `0.0.0.0`                                                                                                             |
  | ZMP_HTTP_SERVER_PORT     | Flask's http server port (not used by wsgi server)                                                  | `5083`                                                                                                                |
  | ZMP_HTTP_SERVER_DEBUG    | Flask's http debug mode (not used by wsgi server)                                                   | `False`                                                                                                               |
  | ZMP_MQTT_SERVER          | MQTT broker's address                                                                               | `localhost`                                                                                                           |
  | ZMP_MQTT_PORT            | MQTT broker's port                                                                                  | `1883`                                                                                                                |
  | ZMP_MQTT_CONNECT_TIMEOUT | Timeout for connection to MQTT broker (in seconds)                                                  | `5`                                                                                                                   |
  | ZMP_MQTT_BASE_TOPIC      | Base topic for MQTT messages                                                                        | `zigbee2mqtt`                                                                                                         |
  | ZMP_MQTT_TLS             | Enable SSL when connecting to MQTT broker                                                           | `False`                                                                                                               |
  | ZMP_MQTT_CA_CERT         | CA certificate to use if TLS is enabled (if not provided, will use system's CAs)                    | `/etc/zigbee2mqtt_maas_power/ssl/mqtt_ca.crt` (if default file does not exists, will use system's CA)                 |
  | ZMP_MQTT_CLIENT_CERT     | Client certificate to use for authentication against the broker (mTLS). Requires TLS to be enabled. | `/etc/zigbee2mqtt_maas_power/ssl/mqtt_client.crt` (if default file does not exists, will not use mTLS authentication) |
  | ZMP_MQTT_CLIENT_KEY      | Client private key to use for authentication against the broker (mTLS). Requires TLS to be enabled. | `/etc/zigbee2mqtt_maas_power/ssl/mqtt_client.key` (if default file does not exists, will not use mTLS authentication) |
  | ZMP_MQTT_USERNAME        | Username to use for password authentication against the broker. Optional.                           | -                                                                                                                     |
  | ZMP_MQTT_PASSWORD        | Password to use for password authentication against the broker. Optional.                           | -                                                                                                                     |