from .author_repository import AuthorRepository
from .books_repository import BookRepository
from .publisher_repository import PublisherRepository

from ..models import Author, Book, Publisher


class UnitOfWork:
    def __init__(self):
        self.authors = AuthorRepository(Author)
        self.books = BookRepository(Book)
        self.publishers = PublisherRepository(Publisher)
