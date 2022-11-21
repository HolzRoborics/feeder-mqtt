from pydantic import BaseSettings


class ToolConfig:
    env_file_encoding = "utf-8"
    extra = "ignore"


class MQTTSettings(BaseSettings):
    HOSTNAME: str = 'mosquitto'
    MAIN_TOPIC_NAME: str = 'ConnectionCreator'

    class Config(ToolConfig):
        env_prefix = "mqtt_"


mqtt_settings = MQTTSettings()
