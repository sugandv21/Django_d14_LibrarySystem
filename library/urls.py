from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, authors_list_create, home

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', home, name='home'),          
    path('api/', include(router.urls)),          
    path('api/authors/', authors_list_create),
]
