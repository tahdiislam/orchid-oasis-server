from rest_framework import serializers
from .models import Flower

class FlowerSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=False)
    class Meta:
        model = Flower
        fields = '__all__'