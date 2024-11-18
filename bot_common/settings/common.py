from pathlib import Path

from pydantic_settings import SettingsConfigDict

from bot_common.settings import bot, broker, db, openai


class CommonSettings(
    bot.TelegramBotSettings,
    broker.BrokerSettings,
    db.DBSettings,
    openai.OpenAISettings,
):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env", env_file_encoding="utf-8", extra="ignore"
    )
