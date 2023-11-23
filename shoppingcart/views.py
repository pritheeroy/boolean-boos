from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from .models import ShoppingCart, Account
from .serializers import ShoppingCartSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

class ViewCartItems(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        # Fetch the account that has is_loggedin set to True
        try:
            account = Account.objects.get(is_loggedin=True)
            return ShoppingCart.objects.filter(account=account)
        except Account.DoesNotExist:
            # Handle the case where no user is logged in
            return ShoppingCart.objects.none()

class UpdateCartItems(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ShoppingCartSerializer


    def update(self, request, *args, **kwargs):
        # Fetch the account that has is_loggedin set to True
        try:
            account = Account.objects.get(is_loggedin=True)
        except Account.DoesNotExist:
            # Handle the case where no user is logged in
            return Response(status=status.HTTP_404_NOT_FOUND)

        for item_data in request.data:
            item_name = item_data.get('item_name')
            is_checked = item_data.get('is_checked')
            ShoppingCart.objects.update_or_create(
                account=account, 
                item_name=item_name, 
                defaults={'is_checked': is_checked}
            )

        return Response({"message": "Cart updated successfully"})

class DeleteCartItem(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        try:
            account = Account.objects.get(is_loggedin=True)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        item_name = kwargs.get('item_name')
        if item_name:
            try:
                cart_item = ShoppingCart.objects.get(account=account, item_name=item_name)
                cart_item.delete()
                return Response({"message": "Item deleted successfully"})
            except ShoppingCart.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)