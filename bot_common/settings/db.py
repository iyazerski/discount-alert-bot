import typing as t

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings
from sqlalchemy.engine.url import URL


class DBSettings(BaseSettings):
    db_username: SecretStr = Field(..., validation_alias="DB_USERNAME")
    db_password: SecretStr = Field(..., validation_alias="DB_PASSWORD")
    db_name: str = Field(..., validation_alias="DB_NAME")
    db_driver: str = Field("postgresql+psycopg2", validation_alias="DB_DRIVER")
    db_host: str = Field(..., validation_alias="DB_HOST")
    db_port: int = Field(..., validation_alias="DB_PORT")

    @property
    def db_dsn(self) -> URL:
        """
        Build DB connection string from settings.
        """

        return URL.create(
            drivername=self.db_driver,
            host=self.db_host,
            port=self.db_port,
            username=self.db_username.get_secret_value(),
            password=self.db_password.get_secret_value(),
            database=self.db_name,
        )

    @property
    def db_connection_params(self) -> dict[str, t.Any]:
        return {
            "dsn": self.db_dsn,
            "pool_pre_ping": True,
            "pool_size": 10,
            "connect_args": {
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        }
