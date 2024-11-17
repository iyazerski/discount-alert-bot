from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class BrokerSettings(BaseSettings):
    broker_username: SecretStr = Field(..., validation_alias="BROKER_USERNAME")
    broker_password: SecretStr = Field(..., validation_alias="BROKER_PASSWORD")
    broker_driver: str = Field("pyamqp", validation_alias="BROKER_DRIVER")
    broker_host: str = Field(..., validation_alias="BROKER_HOST")
    broker_port: int = Field(..., validation_alias="BROKER_PORT")
    broker_vhost: str = Field(..., validation_alias="BROKER_VHOST")

    @property
    def broker_dsn(self) -> str:
        return "{driver}://{username}:{password}@{host}:{port}/{vhost}".format(
            driver=self.broker_driver,
            username=self.broker_username,
            password=self.broker_password,
            host=self.broker_host,
            port=self.broker_port,
            vhost=self.broker_vhost,
        )
