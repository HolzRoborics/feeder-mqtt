from paho.mqtt import subscribe
from paho.mqtt.client import MQTTMessage, Client

from connections.mqtt import mqtt_client
from schemas.error import ErrorMsg
from schemas.topic_init import TopicInit
from logs import logger
from schemas.watchdog import WatchdogInitResponse
from settings import mqtt_settings
from subcriptions.threaded.watchdog import WatchdogSubscription


class MainTopicSubscription:
    def __init__(self, topic_name: str):
        self.topic_name = topic_name

    def callback(self, client: Client, userdata, message: MQTTMessage):
        logger.info(userdata)
        try:
            data = TopicInit.parse_raw(message.payload)
            logger.debug(f'{self.topic_name} | received {data}')

        except Exception as error:
            logger.exception(error)
            return

        logger.debug(f'{self.topic_name} | received {data}')

        if data.WatchDog == 1:
            watchdog_name = f'{data.Name}/WatchDog'

            watchdog = WatchdogSubscription(watchdog_name)
            watchdog.start()

            logger.debug(f'{self.topic_name} | started {watchdog_name}')

            response = WatchdogInitResponse(Name=data.Name)
            mqtt_client.publish(self.topic_name, payload=response.json())
            logger.debug(f'{self.topic_name} | sent {response}')

        else:
            error_msg = ErrorMsg(error='incorrect_data')
            mqtt_client.publish(self.topic_name, payload=error_msg.json())
            logger.debug(f'{self.topic_name} | incorrent_data {data}')

    def run(self):
        subscribe.callback(
            callback=self.callback,
            topics=self.topic_name,
            hostname=mqtt_settings.HOSTNAME,
            auth={'username': mqtt_settings.USERNAME, 'password': mqtt_settings.PASSWORD}
        )
