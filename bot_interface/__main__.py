from bot_interface.bot import Bot
from bot_interface.settings import BotInterfaceSettings


def main() -> None:
    settings = BotInterfaceSettings()  # noqa
    bot = Bot(bot_token=settings.TELEGRAM_BOT_TOKEN)

    bot.run()


if __name__ == "__main__":
    main()
