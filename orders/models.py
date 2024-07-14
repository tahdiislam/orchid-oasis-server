from django.db import models
from customers.models import Customer
from flowers.models import Flower

ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
)
# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    flower = models.ForeignKey(Flower, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=10, choices=ORDER_STATUS,)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} {self.flower} {self.quantity} {self.total_price}"