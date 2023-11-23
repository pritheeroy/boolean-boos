from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Account
from .serializers import AccountSerializer, AccountUpdateSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
import requests  # Import requests
from django.http import JsonResponse
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel("ERROR")


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10

# creating an account
class CreateAccountView(CreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]

    def post(self,request:Request):
        data = request.data

        serializer=self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response={
                "message": "User Created Successfully",
                "data":serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAccountView(RetrieveUpdateAPIView):
    serializer_class = AccountUpdateSerializer
    queryset = Account.objects.all()
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    # def put(self, request:Request):
    #     data = request.data

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Account.objects.get(pk=pk)


class AccountProfileView(ListAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(
                    self.get_serializer(user).data,
                    status=status.HTTP_200_OK
        )

class AccountInfoView(RetrieveAPIView):
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Account, pk=pk)
    

def autocomplete(request):
    input_text = request.GET.get('input', '')
    if not input_text:
        return JsonResponse([])

    google_api_key = 'AIzaSyDpIWKiBj1P0x5buBX2losmBknSRYn1HVI'
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={input_text}&key={google_api_key}&types=address"

    try:
        # print("HELLO")
        response = requests.get(url)
        if response.status_code == 200:
            predictions = response.json().get('predictions', [])
            # print(predictions)
            addresses = [prediction['description'] for prediction in predictions]
            logger.error("Addresses: %s", addresses)
            # print("address", addresses)
            return JsonResponse(addresses, safe=False)
        else:
            return JsonResponse([])
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)})