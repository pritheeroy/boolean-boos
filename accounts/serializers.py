from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['name', 'email', 'username', 'password', 'confirm_password', 'address', 'longitude', 'latitude', 'is_loggedin']

    def validate(self, attrs):
        # Check if email is already in use
        email_exists = Account.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise ValidationError("Email already in use")

        # Check if passwords match
        if attrs.get('password') != attrs.get('confirm_password'):
            raise ValidationError("Passwords do not match")

        return attrs

    def create(self, validated_data):
        # Set is_loggedin to True for every new account
        validated_data['is_loggedin'] = True

        # Remove confirm_password as it's not needed for saving
        if 'confirm_password' in validated_data:
            del validated_data['confirm_password']

        return super(AccountSerializer, self).create(validated_data)

class AccountUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ['name', 'email', 'username', 'password', 'confirm_password', 'address', 'longitude', 'latitude', 'is_loggedin']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
