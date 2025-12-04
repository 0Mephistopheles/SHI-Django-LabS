from rest_framework.response import Response
from rest_framework import status, viewsets
from DB_Management.repositories.unit_of_work import UnitOfWork
from .serializers import AuthorSerializer, BookSerializer, PublisherSerializer, BookOrderSerializer


class AuthorViewSet(viewsets.ViewSet):

    def list(self, request): # GET
        uow = UnitOfWork()
        authors = uow.authors.get_all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None): # GET (by id)
        uow = UnitOfWork()
        author = uow.authors.get_by_id(pk)
        if not author:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    def create(self, request): # POST
        uow = UnitOfWork()
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            uow.authors.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None): # DELETE
        uow = UnitOfWork()
        success = uow.authors.delete_by_id(pk)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None): # PUT
        uow = UnitOfWork()

        author = uow.authors.get_by_id(pk)
        if not author:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AuthorSerializer(instance=author, data=request.data)
        if serializer.is_valid():
            uow.authors.update(pk, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):# PATCH
        uow = UnitOfWork()

        author = uow.authors.get_by_id(pk)
        if not author:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AuthorSerializer(instance=author, data=request.data, partial=True)
        if serializer.is_valid():
            uow.authors.update(pk, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookViewSet(viewsets.ViewSet):

    def list(self, request):
        uow = UnitOfWork()
        books = uow.books.get_all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        uow = UnitOfWork()
        book = uow.books.get_by_id(pk)
        if not book:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def create(self, request):
        uow = UnitOfWork()
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():

            created_book = uow.books.create(serializer.validated_data)
            response_serializer = BookSerializer(created_book)

            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        uow = UnitOfWork()
        success = uow.books.delete_by_id(pk)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None): # PUT
        uow = UnitOfWork()

        book = uow.books.get_by_id(pk)
        if not book:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(instance=book, data=request.data)
        if serializer.is_valid():
            uow.books.update(pk, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):# PATCH
        uow = UnitOfWork()

        book = uow.books.get_by_id(pk)
        if not book:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(instance=book, data=request.data, partial=True)
        if serializer.is_valid():
            uow.books.update(pk, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublisherViewSet(viewsets.ViewSet):

    def list(self, request):
        uow = UnitOfWork()
        publishers = uow.publishers.get_all()
        serializer = PublisherSerializer(publishers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        uow = UnitOfWork()
        publisher = uow.publishers.get_by_id(pk)
        if not publisher:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PublisherSerializer(publisher)
        return Response(serializer.data)

    def create(self, request):
        uow = UnitOfWork()
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            uow.publishers.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        uow = UnitOfWork()
        success = uow.publishers.delete_by_id(pk)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None): # PUT
        uow = UnitOfWork()

        publisher = uow.publishers.get_by_id(pk)
        if not publisher:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PublisherSerializer(instance=publisher, data=request.data)
        if serializer.is_valid():
            uow.publishers.update(pk, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):# PATCH
        uow = UnitOfWork()

        publisher = uow.publishers.get_by_id(pk)
        if not publisher:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PublisherSerializer(instance=publisher, data=request.data, partial=True)
        if serializer.is_valid():
            uow.publishers.update(pk, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookOrderViewSet(viewsets.ViewSet):
    def list(self, request):
        uow = UnitOfWork()
        orders = uow.orders.get_all()
        serializer = BookOrderSerializer(orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        uow = UnitOfWork()
        order = uow.orders.get_by_id(pk)
        if not order:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookOrderSerializer(order)
        return Response(serializer.data)


