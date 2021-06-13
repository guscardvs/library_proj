from enum import Enum
from importlib import import_module


class DriverOptions(str, Enum):
    SQLITE = "sqlite"
    MYSQL = "mysql"
    POSTGRES = "postgresql"


class InvalidDriverName(Exception):
    def __init__(self, driver: str) -> None:
        self.driver = driver

    def __str__(self) -> str:
        return "Invalid driver name {driver}, options are {driver_options}".format(
            driver=self.driver, driver_options=",".join(map(str, DriverOptions))
        )


def driver_parser(val: str):
    val = DriverOptions(val)
    _options = {
        DriverOptions.SQLITE: "aiosqlite",
        DriverOptions.MYSQL: "aiomysql",
        DriverOptions.POSTGRES: "asyncpg",
    }
    driver = _options[val]
    try:
        import_module(driver)
    except ImportError:
        raise InvalidDriverName(val)
    return "{db_type}+{driver}".format(db_type=val.value, driver=driver)
