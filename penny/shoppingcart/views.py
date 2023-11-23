from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ShoppingCart
from django.http import Http404
from .serializers import ShoppingCartSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class AddItemToCartView(CreateAPIView):
    serializer_class = ShoppingCartSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()
    

class RemoveItemFromCartView(DestroyAPIView):
    permission_classes = [AllowAny]

    def get_object(self):
        item_name = self.kwargs.get('item_name')
        cart_item = ShoppingCart.objects.filter(item_name=item_name).first()

        if cart_item is None:
            raise Http404("No ShoppingCart item found with this item name")

        return cart_item


class CheckOffItemView(UpdateAPIView):
    serializer_class = ShoppingCartSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        item_name = self.kwargs.get('item_name')
        cart_item = ShoppingCart.objects.filter(item_name=item_name, is_checked=False).first()

        if cart_item is None:
            raise Http404("No unchecked ShoppingCart item found with this item name")

        return cart_item

    def perform_update(self, serializer):
        serializer.save(is_checked=True)


class UncheckItemView(UpdateAPIView):
    serializer_class = ShoppingCartSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        item_name = self.kwargs.get('item_name')
        cart_item = ShoppingCart.objects.filter(item_name=item_name, is_checked=True).first()

        if cart_item is None:
            raise Http404("No checked ShoppingCart item found with this item name")

        return cart_item

    def perform_update(self, serializer):
        serializer.save(is_checked=False)