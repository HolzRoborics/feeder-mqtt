from time import sleep

from paho.mqtt import subscribe
from paho.mqtt.client import MQTTMessage, Client

from connections.mqtt import mqtt_client
from schemas.subscription_status import SubscriptionStatus
from schemas.topic_init import TopicInit
from logs import logger
from schemas.watchdog import WatchdogInitResponse
from settings import mqtt_settings
from subcriptions.threaded.watchdog import WatchdogSubscription


TOPICS = set()


class MainTopicSubscription:
    def __init__(self, topic_name: str):
        self.topic_name = topic_name

    def callback(self, client: Client, userdata, message: MQTTMessage):
        try:
            data = TopicInit.parse_raw(message.payload)
            logger.debug(f'{self.topic_name} | received {data}')

        except Exception as error:
            logger.exception(error)
            return

        if data.Sender == mqtt_settings.CLIENT_NAME:
            sleep(1)
            return

        if data.WatchDog == SubscriptionStatus.REQUESTED:
            watchdog_name = f'{data.Name}/WatchDog'

            if watchdog_name not in TOPICS:
                watchdog = WatchdogSubscription(watchdog_name)
                watchdog.start()

                logger.debug(f'{self.topic_name} | started {watchdog_name}')

                TOPICS.add(watchdog_name)
            else:
                response = WatchdogInitResponse(Name=data.Name, Sender=mqtt_settings.CLIENT_NAME)
                mqtt_client.publish(self.topic_name, payload=response.json(), retain=True)

                logger.debug(f'{self.topic_name} | sent {response}')

        elif data.WatchDog not in {_ for _ in SubscriptionStatus}:
            response = WatchdogInitResponse(
                Name=data.Name,
                WatchDog=SubscriptionStatus.ERROR,
                Sender=mqtt_settings.CLIENT_NAME,
            )
            mqtt_client.publish(self.topic_name, payload=response.json(), retain=True)

            logger.debug(f'{self.topic_name} | sent {response}')

    def run(self):
        subscribe.callback(
            callback=self.callback,
            topics=self.topic_name,
            hostname=mqtt_settings.HOSTNAME,
            auth={'username': mqtt_settings.USERNAME, 'password': mqtt_settings.PASSWORD}
        )
