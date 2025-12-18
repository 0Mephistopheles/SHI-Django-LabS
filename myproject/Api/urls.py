from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import AnalyticsViewSet

router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet, basename='author')
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'publishers', views.PublisherViewSet, basename='publisher')
router.register(r'orders', views.BookOrderViewSet, basename='order')
router.register(r'analytics', AnalyticsViewSet, basename='analytics') 

urlpatterns = [
    path('', include(router.urls)),
]