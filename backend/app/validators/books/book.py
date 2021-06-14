from datetime import date

from pydantic import Field
from pydantic.class_validators import validator
from validators.common import DTO, IdMixinDTO, get_edit_dto, get_secure_list_dto


class BookDTO(DTO):
    isbn: str = Field(..., max_length=30)
    name: str = Field(..., max_length=255)
    author: str = Field(..., max_length=255)
    publisher: str = Field(..., max_length=255)
    year: int

    @validator("year")
    def validate_year(cls, val: int):
        assert val < date.today().year, "Year cannot be greater than current year"
        assert val > 0, "Year cannot be lesser than 0"
        return val


class BookOutDTO(BookDTO, IdMixinDTO):
    pass


BookEditDTO = get_edit_dto(BookDTO)
BookSecureListDTO = get_secure_list_dto(BookOutDTO)
