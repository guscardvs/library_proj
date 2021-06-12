from typing import Callable, TypeVar

from sqlalchemy import MetaData
from sqlalchemy.orm.decl_api import as_declarative, declared_attr

C_T = TypeVar("C_T")


def _as_declarative(cls: type[C_T]) -> type[C_T]:
    return as_declarative()(cls)  # type: ignore


@_as_declarative
class Entity:
    __name__: str
    metadata: MetaData
    __init__: Callable[..., None]

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
