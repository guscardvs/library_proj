from database.common import Entity
from database.common.mixins.id import IdMixin
from sqlalchemy import Column, Integer, String


class Book(Entity, IdMixin):
    isbn = Column(String(30), unique=True, index=True)
    name = Column(String(255))
    author = Column(String(255))
    publisher = Column(String(255))
    year = Column(Integer)
