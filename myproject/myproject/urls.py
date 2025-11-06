from rest_framework.routers import DefaultRouter
from DB_Management.views import AuthorViewSet, BookViewSet, PublisherViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')
router.register(r'publishers', PublisherViewSet, basename='publisher')

urlpatterns = router.urls
