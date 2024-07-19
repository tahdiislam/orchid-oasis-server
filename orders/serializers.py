from rest_framework import serializers
from .models import Order
from flowers.models import Flower

class FlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = ['id', 'title']

class OrderSerializer(serializers.ModelSerializer):
    flower = FlowerSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'