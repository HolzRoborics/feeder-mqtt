from paho.mqtt import client

from settings import mqtt_settings

mqtt_client = client.Client(mqtt_settings.CLIENT_NAME, userdata=mqtt_settings.USER_DATA)
mqtt_client.username_pw_set(username=mqtt_settings.USERNAME, password=mqtt_settings.PASSWORD)
mqtt_client.connect(mqtt_settings.HOSTNAME)
