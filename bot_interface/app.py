from bot_common.processors import settings
from bot_interface.bot import Bot

bot = Bot(bot_token=settings.TELEGRAM_BOT_TOKEN.get_secret_value())


if __name__ == "__main__":
    bot.run()
