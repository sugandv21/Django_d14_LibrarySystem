from rest_framework import serializers
from .models import Book, Author
from datetime import date

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'created_at']
        read_only_fields = ['id', 'created_at']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True
    )
    book_age = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'author_id', 'genre',
            'published_year', 'book_age', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'author', 'book_age']

    def get_book_age(self, obj):
        if not obj.published_year:
            return None
        return date.today().year - obj.published_year

    def validate_published_year(self, value):
        if value is None:
            return value
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Published year cannot be in the future.")
        return value

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title must not be empty.")
        return value
