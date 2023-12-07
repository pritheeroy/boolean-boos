from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Store
from items.serializers import ItemSerializer


class StoreSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = '__all__'
