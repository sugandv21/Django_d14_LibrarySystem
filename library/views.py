from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Q
from datetime import date
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

# --- Book API (CBV) ---
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    # allow searching by title/genre, but we also implement author filter in get_queryset
    search_fields = ['title', 'genre']

    def get_queryset(self):
        qs = super().get_queryset()
        author_name = self.request.query_params.get('author')
        if author_name:
            qs = qs.filter(author__name__icontains=author_name)
        return qs

# --- Author API (FBV) with browsable API support ---
@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
def authors_list_create(request):
    if request.method == 'GET':
        authors = Author.objects.all().order_by('-created_at')
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    serializer = AuthorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def home(request):
    q = request.GET.get('q', '').strip()
    if q:
        books = Book.objects.filter(
            Q(title__icontains=q) | Q(genre__icontains=q) | Q(author__name__icontains=q)
        ).order_by('-created_at')
    else:
        books = Book.objects.all().order_by('-created_at')

    current_year = date.today().year
    for b in books:
        if b.published_year:
            b.book_age = current_year - b.published_year
        else:
            b.book_age = None

    return render(request, "library/home.html", {"books": books, "q": q})
