import re

from pydantic import BaseModel
from pydantic.main import BaseConfig


class DTO(BaseModel):
    class Config(BaseConfig):
        allow_mutation = False
        allow_population_by_field_name = False

        @classmethod
        def alias_generator(cls, string: str) -> str:
            return re.sub(r"_(\w)", lambda match: match[1].upper(), string)
