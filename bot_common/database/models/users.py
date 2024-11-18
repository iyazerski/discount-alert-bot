import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot_common.database.models import base, mixin

if typing.TYPE_CHECKING:
    from bot_common.database.models.products import Product


class User(base.Base, mixin.CreatedMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)

    products: Mapped[list["Product"]] = relationship(back_populates="user")
