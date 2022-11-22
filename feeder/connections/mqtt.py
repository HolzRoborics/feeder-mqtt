from contextlib import contextmanager

from paho.mqtt import client

from logs import logger
from settings import mqtt_settings


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        logger.debug('Connected')
        return
    elif rc == 1:
        logger.error('Connection refused – incorrect protocol version')
    elif rc == 2:
        logger.error('Connection refused – invalid client identifier')
    elif rc == 3:
        logger.error('Connection refused – server unavailable')
    elif rc == 4:
        logger.error('Connection refused – bad username or password')
    elif rc == 5:
        logger.error('Connection refused – not authorised')
    else:
        logger.error(f'Connection refused – {rc}')
    client.connected_flag = False


@contextmanager
def get_client():
    mqtt_client = client.Client()
    mqtt_client.username_pw_set(username=mqtt_settings.USERNAME, password=mqtt_settings.PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(mqtt_settings.HOSTNAME)
    mqtt_client.loop_start()
    try:
        yield mqtt_client
    finally:
        mqtt_client.disconnect()
