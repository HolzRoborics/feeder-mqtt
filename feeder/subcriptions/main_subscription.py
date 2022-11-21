from paho.mqtt import subscribe
from paho.mqtt.client import MQTTMessage

from connections.mqtt import mqtt_client
from schemas.topic_init import TopicInit
from logs import logger
from schemas.watchdog import WatchdogInitResponse
from settings import mqtt_settings
from subcriptions.threaded.watchdog import WatchdogSubscription


class MainTopicSubscription:
    def __init__(self, topic_name: str):
        self.topic_name = topic_name

    def callback(self, client, userdata, message: MQTTMessage):
        data = TopicInit.parse_raw(message.payload)
        logger.debug(f'{self.topic_name} | received {data}')

        if data.WatchDog is not None:
            watchdog_name = f'{data.Name}/WatchDog'

            watchdog = WatchdogSubscription(watchdog_name)
            watchdog.start()

            logger.debug(f'{self.topic_name} | started {watchdog_name}')

            response = WatchdogInitResponse(Name=data.Name)
            mqtt_client.publish(self.topic_name, payload=response.json())
            logger.debug(f'{self.topic_name} | sent {response}')

    def run(self):
        subscribe.callback(
            callback=self.callback,
            topics=self.topic_name,
            hostname=mqtt_settings.HOSTNAME
        )
