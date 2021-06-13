from functools import partial
from types import FunctionType
from typing import Callable, TypeVar, Union

from core.settings import BASE_DIR
from database.common.entity import Entity
from database.common.model_finder import ModelFinder
from sqlalchemy.orm import relationship as _rel
from sqlalchemy.orm.decl_api import declarative_mixin
from sqlalchemy.sql.schema import Table
from utils.db_driver import DriverOptions

T = TypeVar("T")
Entity_T = TypeVar("Entity_T", bound=Entity)


def get_metadata():

    DATABASE_FOLDER = BASE_DIR / "database"

    model_finder = ModelFinder(DATABASE_FOLDER / "models", DATABASE_FOLDER)
    model_finder.find()
    return Entity.metadata


def get_driver_uri(*, no_parse: bool, driver: str, uri: str):
    if no_parse:
        return f"{driver}://{uri}"
    db_type, _ = driver.split("+")
    _options = {
        DriverOptions.MYSQL.value: "+pymysql",
        DriverOptions.POSTGRES.value: "+psycopg2",
        DriverOptions.SQLITE.value: "",
    }
    if db_type == DriverOptions.SQLITE.value:
        uri = f"/{uri}"
    return f"{db_type}{_options[db_type]}://{uri}"


def as_mixin(cls: type[T]) -> type[T]:
    return declarative_mixin(cls)


def make_relation(
    relation: Union[str, type[Entity_T], Callable[[], type[Entity_T]]],
    *,
    relation_name: str = "",
    back_populates: str,
    secondary: Table = None,
    foreign_key: str = None,
    use_list: bool = False,  # pylint: disable=unused-argument
) -> Union[Entity_T, list[Entity_T]]:
    rel_func = partial(_rel, back_populates=back_populates, lazy="selectin")
    if secondary is not None:
        rel_func = partial(rel_func, secondary=secondary)
    if foreign_key is not None:
        rel_func = partial(rel_func, foreign_keys=[foreign_key])
    if isinstance(relation, str):
        return rel_func(argument=relation)  # type: ignore
    if isinstance(relation, FunctionType):
        return rel_func(argument=relation_name)  # type: ignore
    return rel_func(argument=relation.__qualname__)  # type: ignore
