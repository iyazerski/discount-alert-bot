import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class CreatedMixin:
    created_at: Mapped[dt.datetime | None] = mapped_column(sa.DateTime, server_default=func.now(), nullable=True)
    created_by: Mapped[str | None]


class DeletedMixin:
    deleted_at: Mapped[dt.datetime | None]
    deleted_by: Mapped[str | None]
