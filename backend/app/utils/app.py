from typing import Callable

from fastapi import FastAPI
from typing_extensions import Concatenate, ParamSpec
from utils.middleware import Middleware

P = ParamSpec("P")


class App(FastAPI):
    def add_class_middleware(
        self,
        middleware_cls: Callable[Concatenate["App", P], Middleware],
        *args: P.args,
        **kwargs: P.kwargs
    ):
        middleware_cls(self, *args, **kwargs)
