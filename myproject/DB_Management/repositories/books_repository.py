from DB_Management.models import Book
from .base_repository import BaseRepository

class BookRepository(BaseRepository):
    """
    Конкретна реалізація репозиторія для моделі Book.
    """

    def __init__(self, model):
        self.model = model

    def get_by_id(self, id):
        """
        Отримує книгу за ID (BookID), використовуючи Django ORM.
        """
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None

    def get_all(self):
        """
        Отримує всі книги, використовуючи Django ORM.
        """
        return self.model.objects.all()

    def create(self, data):
        """
        Створює нову книгу.
        'data' - це dict.
        ВАЖЛИВО: для ForeignKey (authorid, publisherid)
        ми повинні передати ЕКЗЕМПЛЯРИ моделей, а не просто ID.
        Приклад: {'title': '...', 'authorid': author_instance, 'publisherid': publisher_instance}
        """
        return self.model.objects.create(**data)

    def delete_by_id(self, id):
        """
        Видаляє об'єкт за ID, використовуючи Django ORM.
        """
        try:
            obj = self.model.objects.get(pk=id)
            obj.delete()
            return True
        except self.model.DoesNotExist:
            return False