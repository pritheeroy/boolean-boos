from django.db import models
from accounts.models import Account # Import Account model

class ShoppingCart(models.Model):
    account = models.ForeignKey(Account, related_name='shopping_cart', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item_name} - {'Checked' if self.is_checked else 'Unchecked'}"
