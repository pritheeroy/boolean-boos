from django.db import models
from items.models import Item


class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.name
