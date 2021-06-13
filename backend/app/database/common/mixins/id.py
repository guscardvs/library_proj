from database.common.functions import as_mixin
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer


@as_mixin
class IdMixin:
    _id = Column(Integer, primary_key=True, autoincrement=True)

    @property
    def pk(self):
        return self.pk

    @classmethod
    def get_pk_column(cls):
        return cls._id
