from django.shortcuts import render
from .serializer import CategorySerializer
from .models import Category
from rest_framework import viewsets

# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer