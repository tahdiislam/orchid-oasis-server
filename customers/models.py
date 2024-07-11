from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='customers/images/', null=True, blank=True)
    phone_no = models.CharField(max_length=12)

    def __str__(self) -> str:
        return f"{self.user.get_full_name()}"