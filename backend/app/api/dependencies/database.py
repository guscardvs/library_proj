from typing import TypeVar

from database.common import DBWrapper, Repository
from fastapi import Request
from utils.overloads import Depends

Repository_T = TypeVar("Repository_T", bound=Repository)


def _get_db_wrapper(request: Request) -> DBWrapper:
    return request.app.state.db_wrapper


def get_repository(repo_cls: type[Repository_T]):
    def _get_repository(db_wrapper: DBWrapper = Depends(_get_db_wrapper)):
        return repo_cls(db_wrapper)

    return _get_repository
