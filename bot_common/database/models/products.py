import datetime as dt
import typing

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot_common.database.models import base, mixin

if typing.TYPE_CHECKING:
    from bot_common.database.models.users import User


class Product(base.Base, mixin.CreatedMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(index=True)
    notification_threshold: Mapped[float]
    initial_price: Mapped[str]
    last_checked_at: Mapped[dt.datetime | None]

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="products")
