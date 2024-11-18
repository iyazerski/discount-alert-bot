from bot_interface.bot import Bot
from bot_interface.settings import BotInterfaceSettings

settings = BotInterfaceSettings()  # noqa
bot = Bot(bot_token=settings.TELEGRAM_BOT_TOKEN)


if __name__ == "__main__":
    bot.run()
