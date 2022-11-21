from subcriptions.main_subscription import MainTopicSubscription

from settings import mqtt_settings


if __name__ == '__main__':
    mts = MainTopicSubscription(mqtt_settings.MAIN_TOPIC_NAME)
    mts.run()
