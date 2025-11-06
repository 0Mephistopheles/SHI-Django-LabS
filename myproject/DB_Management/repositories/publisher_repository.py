from .base_repository import BaseRepository

class PublisherRepository(BaseRepository):
    def __init__(self, model):
        self.model = model

    def get_by_id(self, id):
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None

    def get_all(self):
        return self.model.objects.all()

    def create(self, data):
        return self.model.objects.create(**data)

    def delete_by_id(self, id):
        try:
            obj = self.model.objects.get(pk=id)
            obj.delete()
            return True
        except self.model.DoesNotExist:
            return False

    def update(self, pk, data):
        try:
            obj = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return None

        for key, value in data.items():
            setattr(obj, key, value)

        obj.save()

        return obj