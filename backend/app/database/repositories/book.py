from database.common import Repository
from database.common.filters import Filter
from database.models.books.book import Book
from sqlalchemy.sql.expression import select
from validators.books.book import BookOutDTO, BookSecureListDTO
from validators.common import to_secure_list_dto


class BookRepository(Repository):
    def to_dto(self, obj: Book):
        return BookOutDTO.from_orm(obj)

    async def query(self, *filters: Filter):
        async with self.db_wrapper.transaction_session as session:
            query = select(Book).where(*(f.where(Book) for f in filters))
            result = await session.execute(query)
            return to_secure_list_dto(
                [self.to_dto(item) for item in result.scalars().all()],
                BookSecureListDTO,
            )
