from pydantic import Field
from validators.common.base import DTO


class IdMixinDTO(DTO):
    id_: int = Field(..., alias="id")
