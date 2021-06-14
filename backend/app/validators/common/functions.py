from typing import Generic, TypeVar

from pydantic.main import create_model
from validators.common.base import DTO

DTO_T = TypeVar("DTO_T", bound=DTO)


class SecureDTO(DTO, Generic[DTO_T]):
    data: list[DTO_T]


def get_edit_dto(cls: type[DTO_T]) -> type[DTO_T]:
    """Return a copy of :param:`cls` with all fields `not required`, `nullable` and `default=None`"""

    new_dto = create_model(
        cls.__qualname__.replace("DTO", "EditDTO"),
        __base__=cls,
        __module__=cls.__module__,
    )
    for field in new_dto.__fields__.values():
        field.required = False
        field.default = None
        field.allow_none = True

    return new_dto


def to_secure_list_dto(
    dto_list: list[DTO_T], secure_list_dto: type[SecureDTO[DTO_T]]
) -> SecureDTO[DTO_T]:
    return secure_list_dto(data=dto_list)


def get_secure_list_dto(cls: type[DTO_T]) -> type[SecureDTO[DTO_T]]:
    """
    Return a wrapper `DTO` to be returned as a dict in the api in the format:  `{ 'data': [] }` instead of a root level array.\n
    The type expected to be the value of 'data' is list[:param:`cls`]
    """
    return create_model(
        cls.__qualname__.replace("DTO", "SecureListDTO"),
        __base__=SecureDTO,
        __module__=cls.__module__,
        data=(list[cls], ...),
    )
