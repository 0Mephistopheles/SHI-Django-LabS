from django.db.models import Count, Sum, F, Q, Value
from django.db.models.functions import TruncMonth, Concat
from .base_repository import BaseRepository
from ..models import Author, Book, Bookorder, Publisher, Warehouse, Bookorderitem

class AnalyticsRepository(BaseRepository):

    def get_by_id(self, id):
        raise NotImplementedError("Метод не підтримується в аналітиці")

    def get_all(self):
        raise NotImplementedError("Використовуйте специфічні методи аналітики")

    def create(self, data):
        raise NotImplementedError("Аналітика тільки для читання")

    def delete_by_id(self, id):
        raise NotImplementedError("Аналітика тільки для читання")

    def update(self, id, data):
        raise NotImplementedError("Аналітика тільки для читання")

    def get_books_count_by_author(self, name_query=None, min_books=0):
        queryset = Author.objects.annotate(
            books_count=Count('book'),
            full_name=Concat('firstname', Value(' '), 'lastname')
        )

        if name_query:
            query = name_query.strip()
            queryset = queryset.filter(
                Q(firstname__icontains=query) |
                Q(lastname__icontains=query) |
                Q(full_name__icontains=query)  # Тепер шукає і по повному імені!
            )

        return queryset.filter(books_count__gte=min_books).values(
            'firstname', 'lastname', 'books_count'
        ).order_by('-books_count')

    def get_total_spent_by_customer(self, min_spent=0):
        """Загальна сума замовлень клієнта з фільтром за мін. витратами"""
        return Bookorder.objects.values(
            'customerid__firstname', 'customerid__lastname'
        ).annotate(
            total_spent=Sum('totalamount')
        ).filter(total_spent__gte=min_spent).order_by('-total_spent')

    def get_popularity_by_genre(self, top_n=None):
        """Популярність жанрів (Топ N)"""
        queryset = Book.objects.values('genre').annotate(
            total_sold=Sum('bookorderitem__quantity')
        ).filter(total_sold__gt=0).order_by('-total_sold')
        if top_n:
            queryset = queryset[:int(top_n)]
        return queryset

    def get_monthly_sales_dynamics(self, start_date=None, end_date=None):
        """Динаміка продажів з фільтром за датами"""
        queryset = Bookorder.objects.all()
        if start_date:
            queryset = queryset.filter(orderdate__gte=start_date)
        if end_date:
            queryset = queryset.filter(orderdate__lte=end_date)
        return queryset.annotate(
            month=TruncMonth('orderdate')
        ).values('month').annotate(
            total_revenue=Sum('totalamount')
        ).order_by('month')

    def get_publisher_book_stats(self):
        """Статистика видавництв (без змін)"""
        return Publisher.objects.annotate(
            books_published=Count('book')
        ).values('name', 'books_published').filter(books_published__gt=0).order_by('-books_published')

    def get_low_stock_warehouses(self, threshold=100):
        """Склади з низьким запасом (динамічний поріг)"""
        return Warehouse.objects.annotate(
            total_books=Sum('warehousestock__quantity')
        ).filter(total_books__lt=threshold).values('location', 'total_books').order_by('total_books')

