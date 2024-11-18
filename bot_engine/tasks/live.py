import sqlalchemy as sa

from bot_common.database import models
from bot_common.processors import db
from bot_engine.app import app, price_checker


@app.task(name="add_product")
def add_product(user_telegram_id: int, product_link: str, notification_threshold: int):
    with db.connect():
        user_id = db.execute(sa.select(models.User.id).where(models.User.telegram_id == user_telegram_id)).first()

        if not user_id:
            user_id = db.execute(sa.insert(models.User).values(telegram_id=user_telegram_id)).inserted_primary_key[0]

        db.execute(
            sa.insert(models.Product).values(
                link=product_link,
                notification_threshold=notification_threshold,
                initial_price=price_checker.check_price(product_link),
                user_id=user_id,
            )
        )


@app.task(name="remove_product")
def remove_product(user_telegram_id: int, product_link: str):
    with db.connect():
        db.execute(
            sa.delete(models.Product)
            .where(models.Product.link == product_link)
            .where(models.User.telegram_id == user_telegram_id)
        )


@app.task(name="update_product")
def update_product(user_telegram_id: int, product_link: str, notification_threshold: int):
    with db.connect():
        db.execute(
            sa.update(models.Product)
            .where(models.Product.link == product_link)
            .where(models.User.telegram_id == user_telegram_id)
            .values(notification_threshold=notification_threshold)
        )
