from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Store


class StoreSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Store
        fields = '__all__'
