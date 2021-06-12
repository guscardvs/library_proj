from abc import ABC, abstractmethod
from inspect import iscoroutinefunction
from typing import Any, Callable, Coroutine

from fastapi.applications import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response


class Middleware(ABC):
    def __init__(self, app: FastAPI) -> None:
        self.app = app
        app.middleware("http")(self)

    @abstractmethod
    def before_response(self, request: Request) -> Any:
        ...

    @abstractmethod
    def after_response(
        self, request: Request, response: Response, before_result: Any
    ) -> Any:
        ...

    async def __call__(
        self,
        request: Request,
        call_next: Callable[[Request], Coroutine[None, None, Response]],
    ) -> Response:
        if iscoroutinefunction(self.before_response):
            result = await self.before_response(request)
        else:
            result = self.before_response(request)
        response = await call_next(request)
        if iscoroutinefunction(self.after_response):
            await self.after_response(request, response, result)
        else:
            self.after_response(request, response, result)
        return response
