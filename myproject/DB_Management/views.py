from rest_framework.response import Response
from rest_framework import status, viewsets
from .repositories.unit_of_work import UnitOfWork
from .serializers import AuthorSerializer, BookSerializer, PublisherSerializer


class AuthorViewSet(viewsets.ViewSet):
    uow = UnitOfWork()

    def list(self, request):
        authors = self.uow.authors.get_all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        author = self.uow.authors.get_by_id(pk)
        if not author:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    def create(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            self.uow.authors.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        success = self.uow.authors.delete_by_id(pk)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class BookViewSet(viewsets.ViewSet):
    uow = UnitOfWork()

    def list(self, request):
        books = self.uow.books.get_all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        book = self.uow.books.get_by_id(pk)
        if not book:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            self.uow.books.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        success = self.uow.books.delete_by_id(pk)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class PublisherViewSet(viewsets.ViewSet):
    uow = UnitOfWork()

    def list(self, request):
        publishers = self.uow.publishers.get_all()
        serializer = PublisherSerializer(publishers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        publisher = self.uow.publishers.get_by_id(pk)
        if not publisher:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PublisherSerializer(publisher)
        return Response(serializer.data)

    def create(self, request):
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            self.uow.publishers.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        success = self.uow.publishers.delete_by_id(pk)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
