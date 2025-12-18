from django.db.models import Count, Sum, F
from django.db.models.functions import TruncMonth
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

    def get_books_count_by_author(self):
        """1. Кількість книг кожного автора (Group By + Count)"""
        return Author.objects.annotate(
            books_count=Count('book')
        ).filter(books_count__gt=0).values('firstname', 'lastname', 'books_count').order_by('-books_count')

    def get_total_spent_by_customer(self):
        """2. Загальна сума замовлень кожного клієнта (Group By + Sum)"""
        return Bookorder.objects.values(
            'customerid__firstname',
            'customerid__lastname'
        ).annotate(
            total_spent=Sum('totalamount')
        ).order_by('-total_spent')

    def get_popularity_by_genre(self):
        """3. Популярність жанрів за кількістю проданих книг (Join + Sum)"""
        return Book.objects.values('genre').annotate(
            total_sold=Sum('bookorderitem__quantity')
        ).filter(total_sold__gt=0).order_by('-total_sold')

    def get_monthly_sales_dynamics(self):
        """4. Динаміка продажів по місяцях (Time-series aggregation)"""
        return Bookorder.objects.annotate(
            month=TruncMonth('orderdate')
        ).values('month').annotate(
            total_revenue=Sum('totalamount')
        ).order_by('month')

    def get_publisher_book_stats(self):
        """5. Статистика видавництв за кількістю книг (Count)"""
        return Publisher.objects.annotate(
            books_published=Count('book')
        ).values('name', 'books_published').filter(books_published__gt=0).order_by('-books_published')

    def get_low_stock_warehouses(self, threshold=100):
        """6. Склади з низьким запасом книг (Having через Filter)"""
        return Warehouse.objects.annotate(
            total_books=Sum('warehousestock__quantity')
        ).filter(
            total_books__lt=threshold
        ).values('location', 'total_books').order_by('total_books')