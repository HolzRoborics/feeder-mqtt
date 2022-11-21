from time import sleep
from typing import Optional

from paho.mqtt.client import MQTTMessage, Client

from connections.mqtt import mqtt_client
from logs import logger
from schemas.watchdog import WatchdogData
from .topic_subscription import TopicSubscription


class WatchdogSubscription(TopicSubscription):
    def __init__(self, topic_name: str):
        super().__init__(topic_name)
        self.counter: Optional[int] = None

    def callback(self, client: Client, userdata, message: MQTTMessage):
        try:
            data = WatchdogData.parse_raw(message.payload)
            logger.debug(f'{self.topic_name} | received {data}')

        except Exception as error:
            logger.exception(error)
            return

        if data.Counter == self.counter:
            logger.info(f'{self.topic_name} | received same value')
            sleep(1)
            return

        if data.Counter >= 10000:
            data.Counter = 1
        else:
            data.Counter += 1
        self.counter = data.Counter

        mqtt_client.publish(self.topic_name, payload=data.json(), retain=True)
        logger.debug(f'{self.topic_name} | sent {data}')

