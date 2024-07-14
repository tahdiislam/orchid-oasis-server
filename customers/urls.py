from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register('list', views.CustomerViewSet)


urlpatterns = [
    path('', include(router.urls), name='customers'),
    path('register/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('confirm/<uid64>/<token>/', views.activate, name='activate'),
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('logout/', views.UserLogoutAPIView.as_view(), name='logout'),
]