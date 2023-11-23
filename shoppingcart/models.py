from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class ShoppingCart(models.Model):
    item_name = models.CharField(max_length=100) 
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item_name} - {'Checked' if self.is_checked else 'Unchecked'}"