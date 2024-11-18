from celery import Celery

from bot_common.processors import broker

broker.config("bot_engine.celeryconfig")
app: Celery = broker.app


if __name__ == "__main__":
    app.start()
