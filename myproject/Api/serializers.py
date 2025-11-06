from rest_framework import serializers
from DB_Management.models import Author, Book, Publisher

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(source='authorid', read_only=True)
    publisher = PublisherSerializer(source='publisherid', read_only=True)

    authorid = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), write_only=False
    )
    publisherid = serializers.PrimaryKeyRelatedField(
        queryset=Publisher.objects.all(), write_only=False
    )
    class Meta:
        model = Book
        fields = '__all__'
