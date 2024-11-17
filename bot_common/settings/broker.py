from pydantic import SecretStr
from pydantic_settings import BaseSettings


class BrokerSettings(BaseSettings):
    BROKER_USERNAME: SecretStr
    BROKER_PASSWORD: SecretStr
    BROKER_DRIVER: str = "pyamqp"
    BROKER_HOST: str
    BROKER_PORT: int
    BROKER_VHOST: str

    @property
    def broker_dsn(self) -> str:
        return "{driver}://{username}:{password}@{host}:{port}/{vhost}".format(
            driver=self.BROKER_DRIVER,
            username=self.BROKER_USERNAME.get_secret_value(),
            password=self.BROKER_PASSWORD.get_secret_value(),
            host=self.BROKER_HOST,
            port=self.BROKER_PORT,
            vhost=self.BROKER_VHOST,
        )
