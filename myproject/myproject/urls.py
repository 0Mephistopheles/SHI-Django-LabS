from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.contrib import admin
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("Api.urls")),
    path("", include("Interfaces.urls"))
]
