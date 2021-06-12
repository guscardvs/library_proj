from typing import Union

from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class UnsetEnvironmentError(Exception):
    def __init__(self, key: str) -> None:
        self.key = key

    def __str__(self) -> str:
        return f"The env key {self.key} is unset"


class UnsetConnectionError(Exception):
    def __init__(self, service_name: str) -> None:
        self.service_name = service_name

    def __str__(self) -> str:
        return f"The connection of the service {self.service_name} is not set"


class ApiError(Exception):

    status_code = HTTP_400_BAD_REQUEST

    __msg: str

    def get_message(self) -> str:
        try:
            return self.__msg
        except AttributeError:
            return "An error occurred"

    def set_msg(self, msg: str):
        self.__msg = msg

    @classmethod
    def from_message(cls, message: str, status_code: int = None):
        exc = ApiError()
        exc.set_msg(message)
        exc.status_code = status_code or cls.status_code
        return exc


class RepositoryException(ApiError):
    _object: str

    @classmethod
    def preload_cls(cls, obj: Union[str, type]):
        exc = cls()
        if isinstance(obj, str):
            exc._object = obj
            return exc
        result_string = obj.__qualname__
        for item in obj.mro()[1:]:
            result_string = result_string.replace(item.__qualname__, "")
        exc._object = result_string
        return exc


class DoesNotExist(RepositoryException):
    status_code = HTTP_404_NOT_FOUND

    def get_message(self) -> str:
        return f"{self._object} not found"


class AlreadyExists(RepositoryException):
    status_code = HTTP_409_CONFLICT

    def get_message(self) -> str:
        return f"{self._object} already exists"


class UnexpectedError(ApiError):
    def __init__(self) -> None:
        pass

    status_code = HTTP_500_INTERNAL_SERVER_ERROR

    message = "An unexpected error occured, talk to the tech team"

    def get_message(self) -> str:
        return self.message

    @classmethod
    def from_module(cls, module: str):
        return cls.from_message("Unhandled exception in {}".format(module))


class UnAuthorizedError(ApiError):
    def __init__(self) -> None:
        pass

    status_code = HTTP_403_FORBIDDEN

    def get_message(self) -> str:
        return "You do not have permission to use this route"


class InvalidPassword(ApiError):
    def __init__(self) -> None:
        pass

    status_code = HTTP_403_FORBIDDEN

    def get_message(self) -> str:
        return "Invalid Password"


class UnsetPassword(ApiError):
    def __init__(self) -> None:
        pass

    status_code = HTTP_400_BAD_REQUEST

    def get_message(self) -> str:
        return "User has not set password yet"


class NotAuthenticated(ApiError):
    def __init__(self) -> None:
        pass

    status_code = HTTP_401_UNAUTHORIZED

    def get_message(self) -> str:
        return "not authenticated"


class InvalidOrExpiredToken(NotAuthenticated):
    def get_message(self) -> str:
        return "Invalid or expired token"
