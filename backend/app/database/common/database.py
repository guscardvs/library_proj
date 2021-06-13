from contextlib import asynccontextmanager
from typing import Optional

from core.settings import DB_DRIVER, DB_URI
from database.common.functions import get_driver_uri
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from utils.db_driver import DriverOptions


class DBWrapper:
    def __init__(self, conn_uri: Optional[str] = None) -> None:
        self.engine = self._create_engine(conn_uri)
        self.sessionmaker = self._create_sessionmaker()

    def _create_engine(self, conn_uri: Optional[str]):
        if conn_uri:
            return create_async_engine(conn_uri)
        return create_async_engine(
            get_driver_uri(no_parse=True, driver=DB_DRIVER, uri=DB_URI),
            pool_size=20,
            max_overflow=0,
        )

    def _create_sessionmaker(self):
        return sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
        )

    @asynccontextmanager
    async def _transaction_session(self):
        async with self.sessionmaker() as session:
            async with session.begin():
                yield session

    @property
    def transaction_session(self):
        return self._transaction_session()
