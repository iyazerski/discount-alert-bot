from loguru import logger
from telegram.ext import Application, ApplicationBuilder, CommandHandler

from bot_interface import handlers


class Bot:
    def __init__(self, bot_token: str) -> None:
        self._app: Application = ApplicationBuilder().token(bot_token).build()

    def run(self) -> None:
        logger.info("Telegram Bot started")

        self.register_handlers()
        self._app.run_polling()

    def register_handlers(self) -> None:
        self._app.add_handler(CommandHandler("start", handlers.start))
        self._app.add_handler(CommandHandler("add", handlers.add))
        self._app.add_handler(CommandHandler("list", handlers.list_products))
        self._app.add_handler(CommandHandler("remove", handlers.remove))
        self._app.add_handler(CommandHandler("update", handlers.update_product))

        logger.info("Successfully registered handlers for Telegram commands")
