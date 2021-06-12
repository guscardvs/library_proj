from utils.exceptions import UnsetEnvironmentError
from enum import Enum
from os import getenv
from typing import Callable, TypeVar

T = TypeVar("T")


class Env(str, Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


class RequiredEnv:
    def __init__(self) -> None:
        self._setenv()

    def _setenv(self):
        env = getenv("ENV", "dev")
        self.env = Env(env)

    def required_if_conditional(
        self,
        key: str,
        cond: bool,
        default: str,
        *,
        parser: Callable[[str], T] = lambda v: v
    ) -> T:
        val = getenv(
            key,
        )
        if cond and val is None:
            raise UnsetEnvironmentError(key)
        return parser(val or default)

    def __call__(
        self, key: str, default: str, *, parser: Callable[[str], T] = lambda v: v
    ) -> T:
        return self.required_if_conditional(
            key, self.env == Env.PROD, default, parser=parser
        )
