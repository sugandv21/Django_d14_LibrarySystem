from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id','name','created_at')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id','title','author','published_year','created_at')
    search_fields = ('title','author__name','genre')
    list_filter = ('genre','published_year')
