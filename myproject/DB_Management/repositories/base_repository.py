import abc

class BaseRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, data):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_by_id(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, id, data):
        raise NotImplementedError
