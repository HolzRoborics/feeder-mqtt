from paho.mqtt import client

from settings import mqtt_settings

mqtt_client = client.Client('Feeder')
mqtt_client.connect(mqtt_settings.HOSTNAME)
