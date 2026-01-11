from django.db.models import Count, Sum, F, Q, Value
from django.db.models.functions import TruncMonth, Concat
from .base_repository import BaseRepository
from ..models import Author, Book, Bookorder, Publisher, Warehouse, Bookorderitem


class AnalyticsRepository(BaseRepository):
    def get_by_id(self, id):
        raise NotImplementedError
    def get_all(self):
        raise NotImplementedError
    def create(self, data):
        raise NotImplementedError
    def delete_by_id(self, id):
        raise NotImplementedError
    def update(self, id, data):
        raise NotImplementedError

    def get_books_count_by_author(self, name_query=None, min_books=0):
        # .order_by() тут запобігає зайвому сортуванню, якщо воно є в Meta автора
        queryset = Author.objects.order_by().annotate(
            books_count=Count('book'),
            full_name=Concat('firstname', Value(' '), 'lastname')
        )
        if name_query:
            query = name_query.strip()
            queryset = queryset.filter(
                Q(firstname__icontains=query) |
                Q(lastname__icontains=query) |
                Q(full_name__icontains=query)
            )
        return queryset.filter(books_count__gte=min_books).values(
            'firstname', 'lastname', 'books_count'
        ).order_by('-books_count')

    def get_total_spent_by_customer(self, min_spent=0):
        # ВАЖЛИВО: .order_by() перед .values() запобігає розбиттю на окремі замовлення
        return Bookorder.objects.filter(paymentstatus='Paid') \
            .order_by() \
            .values('customerid__firstname', 'customerid__lastname') \
            .annotate(total_spent=Sum('totalamount')) \
            .filter(total_spent__gte=min_spent) \
            .order_by('-total_spent')

    def get_popularity_by_genre(self, top_n=None):

        queryset = Book.objects.filter(bookorderitem__orderid__paymentstatus='Paid') \
            .order_by() \
            .values('genre') \
            .annotate(total_sold=Sum('bookorderitem__quantity')) \
            .filter(total_sold__gt=0) \
            .order_by('-total_sold')

        if top_n:
            queryset = queryset[:int(top_n)]
        return queryset

    def get_monthly_sales_dynamics(self, start_date=None, end_date=None):
        queryset = Bookorder.objects.filter(paymentstatus='Paid')

        if start_date:
            queryset = queryset.filter(orderdate__gte=start_date)
        if end_date:
            queryset = queryset.filter(orderdate__lte=end_date)

        # .order_by() перед TruncMonth важливий, щоб не сортувати по даті створення замовлення
        return queryset.annotate(
            month=TruncMonth('orderdate')
        ).order_by().values('month').annotate(
            total_revenue=Sum('totalamount')
        ).order_by('month')

    def get_publisher_book_stats(self):
        return Publisher.objects.order_by().annotate(
            books_published=Count('book')
        ).values('name', 'books_published').filter(books_published__gt=0).order_by('-books_published')

    def get_low_stock_warehouses(self, threshold=100):
        return Warehouse.objects.order_by().annotate(
            total_books=Sum('warehousestock__quantity')
        ).filter(total_books__lt=threshold).values('location', 'total_books').order_by('total_books')