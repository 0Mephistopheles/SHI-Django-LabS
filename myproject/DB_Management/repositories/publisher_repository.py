from DB_Management.models import Publisher
from .base_repository import BaseRepository

class PublisherRepository(BaseRepository):
    """
    Конкретна реалізація репозиторія для моделі Publisher.
    """

    def __init__(self, model):
        self.model = model

    def get_by_id(self, id):
        """
        Отримує видавця за ID (PublisherID), використовуючи Django ORM.
        """
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None

    def get_all(self):
        """
        Отримує всіх видавців, використовуючи Django ORM.
        """
        return self.model.objects.all()

    def create(self, data):
        """
        Створює нового видавця.
        'data' - це dict, наприклад: {'name': 'А-БА-БА-ГА-ЛА-МА-ГА'}
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