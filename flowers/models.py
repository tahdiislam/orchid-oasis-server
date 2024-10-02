from django.db import models
from categories.models import Category

class Flower(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(max_length=500, null=True)  # Updated to store the image URL
    price = models.FloatField()
    available = models.IntegerField(default=1)

    def __str__(self):
        return self.title