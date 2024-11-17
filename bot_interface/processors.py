from bot_common.broker import Broker
from bot_common.database import Database
from bot_interface.bot import Bot
from bot_interface.settings import BotInterfaceSettings

settings = BotInterfaceSettings()
bot = Bot(bot_token=settings.TELEGRAM_BOT_TOKEN)
broker = Broker(dsn=settings.broker_dsn)
db = Database(dsn=settings.db_dsn, **settings.db_connection_params)
