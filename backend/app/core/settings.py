from pathlib import Path

from utils.db_driver import driver_parser
from utils.env import RequiredEnv

BASE_DIR = Path(__file__).resolve().parent.parent


required_env = RequiredEnv()

DB_URI = required_env("DB_URI", "{}".format((BASE_DIR / "db.sqlite").as_posix()))

DB_DRIVER = required_env("DB_DRIVER", "sqlite", parser=driver_parser)
