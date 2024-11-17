import typing as t

from pydantic import SecretStr
from pydantic_settings import BaseSettings
from sqlalchemy.engine.url import URL


class DBSettings(BaseSettings):
    DB_USERNAME: SecretStr
    DB_PASSWORD: SecretStr
    DB_NAME: str
    DB_DRIVER: str = "postgresql+psycopg2"
    DB_HOST: str
    DB_PORT: int

    @property
    def db_dsn(self) -> URL:
        """
        Build DB connection string from settings.
        """

        return URL.create(
            drivername=self.DB_DRIVER,
            host=self.DB_HOST,
            port=self.DB_PORT,
            username=self.DB_USERNAME.get_secret_value(),
            password=self.DB_PASSWORD.get_secret_value(),
            database=self.DB_NAME,
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
