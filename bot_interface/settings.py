from pydantic_settings import BaseSettings

from bot_common.settings import CommonSettings


class BotInterfaceSettings(BaseSettings, CommonSettings):
    TELEGRAM_BOT_TOKEN: str
