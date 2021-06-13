from database.common import Repository
from database.common.filters import Filter
from database.models.books.book import Book


class BookRepository(Repository):
    def to_dto(self, obj: Book):
        return

    async def query(self, *filters: Filter):
        return ...
