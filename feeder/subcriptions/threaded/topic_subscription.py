from threading import Thread

from paho.mqtt import subscribe
from paho.mqtt.client import MQTTMessage, Client

from settings import mqtt_settings


class TopicSubscription(Thread):
    def __init__(self, topic_name: str):
        super().__init__()
        self.topic_name = topic_name

    def callback(self, client: Client, userdata, message: MQTTMessage):
        raise NotImplementedError

    def run(self) -> None:
        subscribe.callback(
            callback=self.callback,
            topics=self.topic_name,
            hostname=mqtt_settings.HOSTNAME,
            auth={'username': mqtt_settings.USERNAME, 'password': mqtt_settings.PASSWORD}
        )
