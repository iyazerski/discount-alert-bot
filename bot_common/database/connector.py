import typing as t
from contextlib import contextmanager

import sqlalchemy as sa
from loguru import logger
from sqlalchemy.engine import URL
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.orm import Session, scoped_session, sessionmaker


class Database:
    def __init__(self, dsn: URL, **connection_params: t.Any) -> None:
        self._host = f"{dsn.host}:{dsn.port}"
        self._engine = sa.create_engine(dsn, **connection_params)
        self.Session = scoped_session(sessionmaker(bind=self._engine, autocommit=False, autoflush=False))

    @contextmanager
    def connect(self) -> Session:
        """
        Context manager responsible for safe execution of DB operations inside the ORM session scope

        Examples:
            >>> from sqlalchemy import text
            >>>
            >>> db = Database(dsn=URL())
            >>> with db.connect() as session:
            >>>     session.execute(text("SELECT 1"))
            >>>
            >>>     session2 = db.Session()
            >>>     assert id(session) == id(session2)
        """

        self.healthcheck()
        logger.debug(f"Connected to DB at {self._host}")

        try:
            yield self.Session
        except Exception as exc:
            self.Session.rollback()
            self.disconnect()
            raise exc

        try:
            self.Session.commit()
        except PendingRollbackError as exc:
            self.Session.rollback()
            self.disconnect()
            raise exc

        self.disconnect()

    def disconnect(self) -> None:
        self.Session.remove()
        logger.debug(f"Disconnected from DB at {self._host}")

    def healthcheck(self) -> sa.ScalarResult | sa.Result:
        """
        Check that the database is connected and ready
        """
        try:
            return self.execute(sa.select(1))
        except Exception as exc:
            raise RuntimeError(f"Failed to connect to DB at {self._host}: {exc}") from None

    def execute(
        self, query: sa.Select | sa.Insert | sa.Update | sa.Delete, scalars: bool = True
    ) -> sa.ScalarResult | sa.Result:
        """
        Execute the provided `query` and return the scalar result
        """

        # handle update/delete commands
        if isinstance(query, (sa.Insert, sa.Update, sa.Delete)):
            with self.Session.begin_nested():
                return self.Session.execute(query)

        return self.Session.scalars(query) if scalars else self.Session.execute(query)
