from telegram.ext import Application, ApplicationBuilder, CommandHandler


class Bot:
    def __init__(self, bot_token: str) -> None:
        self._app: Application = ApplicationBuilder().token(bot_token).build()

    async def start(self) -> None:
        await self._app.initialize()
        await self._app.start()

    async def stop(self) -> None:
        await self._app.stop()
        await self._app.shutdown()

    def register_handlers(self) -> None:
        from bot_interface import handlers

        self._app.add_handler(CommandHandler("start", handlers.start))
        self._app.add_handler(CommandHandler("add", handlers.add))
        self._app.add_handler(CommandHandler("list", handlers.list_products))
        self._app.add_handler(CommandHandler("remove", handlers.remove))
        self._app.add_handler(CommandHandler("update", handlers.update_product))
