from rest_framework import serializers
from .models import ShoppingCart

class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ['account', 'item_name', 'is_checked']
