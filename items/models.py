from django.db import models
import uuid


class Item(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('lb', 'Pound'),
        ('g', 'Gram'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # store = models.ForeignKey(Store, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    unit_system = models.CharField(max_length=255)

    def __str__(self):
        return self.name + self.store
