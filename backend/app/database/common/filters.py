import operator
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Union

from database.common.entity import Entity
from sqlalchemy import Column, and_, false, or_, true
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.elements import BooleanClauseList


class Filter:
    def where(self, entity: type[Entity]):
        pass


class CompareOptions(str, Enum):
    EQUAL = "eq"
    NOT_EQUAL = "ne"
    GREATER = "gt"
    GREATER_EQUAL = "ge"
    LESSER = "lt"
    LESSER_EQUAL = "le"
    CONTAINS = "contains"
    ICONTAINS = "icontains"


@dataclass
class FieldFilter(Filter):
    field: str
    value: Optional[Any]
    related: str = ""
    comparison: CompareOptions = CompareOptions.EQUAL

    def __post_init__(self):
        if isinstance(self.value, bool):
            self.value = true() if self.value else false()

    def where(self, entity: type[Entity]):
        return self.related_attr(entity) if self.related else self.attr(entity)

    def related_attr(self, entity: type[Entity]):
        related_entity = self._attr(entity, self.related)
        return self.attr(related_entity.entity.class_)  # type: ignore

    def attr(self, entity: type[Entity]):
        attr = self._attr(entity, self.field)
        if self.value is None:
            return True
        if self.comparison not in [CompareOptions.CONTAINS, CompareOptions.ICONTAINS]:
            return getattr(operator, self.comparison.value)(attr, self.value)
        if self.comparison == CompareOptions.CONTAINS:
            return attr.like(f"%{self.value}%")
        return attr.ilike(f"%{self.value}%")

    @staticmethod
    def _attr(entity: type[Entity], field: str) -> Union[Column, RelationshipProperty]:
        result = getattr(entity, field, None)
        if not result:
            raise NotImplementedError
        return result


@dataclass(init=False)
class FilterJoins(Filter):
    operator: type[BooleanClauseList]
    filters: tuple[Filter, ...]

    def __init__(self, *filters: Filter) -> None:
        self.filters = filters

    def where(self, entity: type[Entity]):
        return self.operator(*(f.where(entity) for f in self.filters))


class OrFilter(FilterJoins):
    @property
    def operator(self):
        return or_


class AndFilter(FilterJoins):
    @property
    def operator(self):
        return and_
