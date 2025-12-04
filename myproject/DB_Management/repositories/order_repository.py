from .base_repository import BaseRepository
from ..models import Bookorder, Customer


class OrderRepository(BaseRepository):
    def __init__(self, model):
        self.model = model

    def get_by_id(self, id):
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None

    def get_all(self):
        return self.model.objects.all()

    def get_by_email(self, email):
        # Знаходимо клієнта за email, потім його замовлення
        customer = Customer.objects.filter(email=email).first()
        if customer:
            return self.model.objects.filter(customerid=customer).order_by('-orderdate')
        return []

    def create(self, data):
        return self.model.objects.create(**data)

    def delete_by_id(self, id):
        # Видалення замовлень зазвичай не рекомендується, але для лаби реалізуємо
        try:
            obj = self.model.objects.get(pk=id)
            obj.delete()
            return True
        except self.model.DoesNotExist:
            return False

    def update(self, pk, data):
        # Оновлення статусу тощо
        try:
            obj = self.model.objects.get(pk=pk)
            for key, value in data.items():
                setattr(obj, key, value)
            obj.save()
            return obj
        except self.model.DoesNotExist:
            return None