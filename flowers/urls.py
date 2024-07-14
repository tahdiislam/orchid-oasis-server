from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include

router = DefaultRouter()

router.register('list', views.FlowerViewSet)

urlpatterns = [
    path('', include(router.urls), name='flowers'),
]