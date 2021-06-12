from utils.db_driver import driver_parser
from utils.env import RequiredEnv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


required_env = RequiredEnv()

DB_URI = required_env("DB_URI", str(BASE_DIR / "db.sqlite"))

DB_DRIVER = required_env("DB_DRIVER", "mysql", parser=driver_parser)
