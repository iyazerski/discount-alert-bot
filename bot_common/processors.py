from bot_common.broker import Broker
from bot_common.database import Database
from bot_common.settings import CommonSettings

settings = CommonSettings()  # noqa
broker = Broker(dsn=settings.broker_dsn)
db = Database(**settings.db_connection_params)
