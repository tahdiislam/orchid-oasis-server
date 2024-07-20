from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(max_length=60, unique=True)
    image = models.ImageField(upload_to='categories/images/', null=True, blank=True)

    def __str__(self):
        return self.name