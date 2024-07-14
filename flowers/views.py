from django.shortcuts import render
from .serializers import FlowerSerializer
from .models import Flower
from rest_framework import viewsets

# Create your views here.
class FlowerViewSet(viewsets.ModelViewSet):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer