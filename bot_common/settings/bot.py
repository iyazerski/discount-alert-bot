from pydantic import SecretStr
from pydantic_settings import BaseSettings


class TelegramBotSettings(BaseSettings):
    TELEGRAM_BOT_TOKEN: SecretStr
