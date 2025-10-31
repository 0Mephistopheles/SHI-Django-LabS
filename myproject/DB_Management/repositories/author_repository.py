from DB_Management.models import Author
from .base_repository import BaseRepository

class AuthorRepository(BaseRepository):
    """
    Конкретна реалізація репозиторія для моделі Author.
    """

    def __init__(self, model):
        # Ми передаємо модель сюди з UnitOfWork
        self.model = model

    def get_by_id(self, id):
        """
        Отримує автора за ID (AuthorID), використовуючи Django ORM.
        """
        try:
            # pk=id автоматично знайде поле, що є primary_key (у нас це authorid)
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None

    def get_all(self):
        """
        Отримує всіх авторів, використовуючи Django ORM.
        """
        return self.model.objects.all()

    def create(self, data):
        """
        Створює нового автора, використовуючи Django ORM.
        'data' - це dict, наприклад: {'firstname': 'Тарас', 'lastname': 'Шевченко'}
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