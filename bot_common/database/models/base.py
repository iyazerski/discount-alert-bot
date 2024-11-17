import json
import typing as t

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    @classmethod
    def columns(cls) -> set[str]:
        """
        List the table columns names
        """

        return {col.name for col in inspect(cls).columns}

    def to_dict(self, exclude: set[str] | None = None, exclude_none: bool = False) -> dict[str, t.Any]:
        """
        Convert the database entry into a Python dictionary
        """

        allowed_columns = self.columns().difference(exclude or set())
        result = {k: v for k, v in self.__dict__.items() if k in allowed_columns}
        if exclude_none:
            result = {k: v for k, v in result.items() if v is not None}
        return result

    def to_json(self, *args, indent: int | None = None, **kwargs: t.Any) -> str:
        """
        Convert the database entry into a JSON string (firstly converted into a Python dictionary)
        """

        return json.dumps(self.to_dict(*args, **kwargs), indent=indent, default=str)
