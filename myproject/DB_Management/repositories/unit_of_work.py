from django.db import transaction

from .analytics_repository import AnalyticsRepository
from .author_repository import AuthorRepository
from .bookOrderItem_repository import BookOrderItemRepository
from .books_repository import BookRepository
from .publisher_repository import PublisherRepository
from .order_repository import OrderRepository
from .warehouseStock_repository import WarehouseStockRepository
from .warehouse_repository import WarehouseRepository

from ..models import Author, Book, Publisher, Bookorder, Bookorderitem, Warehouse, Warehousestock


class UnitOfWork:
    def __init__(self):
        self.authors = AuthorRepository(Author)
        self.books = BookRepository(Book)
        self.publishers = PublisherRepository(Publisher)
        self.orders = OrderRepository(Bookorder)

        self.order_items = BookOrderItemRepository(Bookorderitem)
        self.warehouses = WarehouseRepository(Warehouse)
        self.stocks = WarehouseStockRepository(Warehousestock)

        self.analytics = AnalyticsRepository()

        self._transaction = None

    def __enter__(self):
        self._transaction = transaction.atomic()
        self._transaction.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self._transaction.__exit__(exc_type, exc_val, exc_tb)
        else:
            self._transaction.__exit__(None, None, None)
