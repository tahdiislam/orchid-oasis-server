from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('list', views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls), name='orders'),
    path('create/', views.OrderCreateAPIView.as_view(), name='create'),
    path('change-status/<order_id>', views.ChangeOrderStatus, name='change_order_status')
]