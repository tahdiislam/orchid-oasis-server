from django.shortcuts import render
from .serializers import FlowerSerializer
from .models import Flower
from rest_framework import viewsets, pagination

# Create your views here.
class FlowerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Flower.objects.all().order_by('price')
    serializer_class = FlowerSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        limit = self.request.query_params.get('limit')
        if limit is not None:
            try:
                queryset = queryset[:int(limit)]
            except ValueError:
                pass
        return queryset