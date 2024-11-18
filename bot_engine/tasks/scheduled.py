import sqlalchemy as sa

from bot_common.database import models
from bot_common.processors import db
from bot_engine.app import app


@app.task(names="check_price")
def check_price():
    with db.connect():
        db.execute(sa.select(models.Product)).all()
