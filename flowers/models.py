from django.db import models
from categories.models import Category

# Create your models here.
class Flower(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='flowers/images/')
    price = models.FloatField()
    available = models.IntegerField(default=1)

    def __str__(self):
        return self.name