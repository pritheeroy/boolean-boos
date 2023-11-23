from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.validators import ValidationError
from .models import ShoppingCart


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'
    

