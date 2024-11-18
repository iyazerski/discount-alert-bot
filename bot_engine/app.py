from celery import Celery

from bot_common.processors import broker, settings
from bot_engine.price_check import PriceChecker

broker.config("bot_engine.celeryconfig")
app: Celery = broker.app
price_checker = PriceChecker(openai_api_token=settings.OPENAI_API_TOKEN, openai_model=settings.OPENAI_MODEL)


if __name__ == "__main__":
    app.start()
