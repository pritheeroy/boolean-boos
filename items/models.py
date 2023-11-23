from django.db import models
import uuid


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    # store = models.ForeignKey(Store, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    unit_system = models.CharField(max_length=255)

    def __str__(self):
        return self.name + self.store
