from abc import ABC, abstractmethod
from typing import final

from database.common.database import DBWrapper
from database.common.filters import Filter
from utils.exceptions import AlreadyExists, DoesNotExist


class Repository(ABC):
    @final
    def __init__(self, db_wrapper: DBWrapper) -> None:
        self.db_wrapper = db_wrapper
        self._create_exceptions()

    @final
    def _create_exceptions(self):
        self.does_not_exist = DoesNotExist.preload_cls(self.__class__)
        self.already_exists = AlreadyExists.preload_cls(self.__class__)

    @abstractmethod
    async def query(self, *filters: Filter):
        raise NotImplementedError

    @abstractmethod
    def to_dto(self, obj):
        raise NotImplementedError
