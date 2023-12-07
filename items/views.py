from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Item
from stores.models import Store
from .serializers import ItemSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status
from django.http import Http404, HttpResponse
from django.db import connection
import requests
from requests.exceptions import RequestException



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = "page_size"
    max_page_size = 10


class ItemView(ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['price', 'location']  # Sort by Price and Location
    # filterset_fields = ['name']  # Search by name or store
    permission_classes = [AllowAny]

    def get_queryset(self):
        search_term = self.request.query_params.get('name')
        queryset = Item.objects.all()

        try:
            if search_term:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id FROM Items_item WHERE LOWER(name) ILIKE LOWER(%s)",
                        [f"%{search_term.lower()}%"]
                    )
                    results = [row[0] for row in cursor.fetchall()]

                # Filter the queryset based on the IDs from the SQL query
                queryset = queryset.filter(id__in=results)
        except:
            return queryset.filter(id__in=[])

        return queryset

    # def get_queryset(self):
    #     search_term = self.request.query_params.get('name')

    #     queryset = Item.objects.all()

    #     if search_term:
    #         queryset = queryset.filter(name__icontains=search_term)

    #     return queryset


class ItemDetailView(ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['name']
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # Sort by Price and Location
    ordering_fields = ['price', 'location']
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        search_term = self.request.query_params.get('name')

        # Filter stores based on items that contain the search input
        stores = Store.objects.filter(items__name__icontains=search_term)

        # Initialize a list to store store names and prices
        store_data = []

        for store in stores:
            # Fetch the price for the current item and store
            price_for_store = store.items.filter(
                name__icontains=search_term).values('price').first()

            # Check if the item exists in the store
            if price_for_store is not None and {'store_name': store.name, 'price': price_for_store['price']} not in store_data:
                store_data.append(
                    {'store_name': store.name, 'price': price_for_store['price']})

        ordering_param = self.request.query_params.get(
            'ordering', 'price')
        reverse_order = ordering_param.startswith('-')

        if reverse_order:
            store_data = sorted(
                store_data, key=lambda x: x.get('price', 0), reverse=True)
        else:
            store_data = sorted(store_data, key=lambda x: x.get('price', 0))

        return Response({'stores_with_item': store_data}, status=status.HTTP_200_OK)


class ItemUpdateView(RetrieveUpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]

    def update(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')  # assuming the URL parameter is named 'pk'

        if not item_id:
            return Response(
                {'detail': 'Item ID (pk) not provided in the request.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Assuming 'pk' is a UUIDField in your model
            item = get_object_or_404(Item, pk=item_id)
        except ValueError:
            raise Http404  # Return a 404 response if the UUID is not valid

        serializer = self.get_serializer(item, data=request.data, partial=True)

        if serializer.is_valid():
            # Additional logic for handling new fields
            is_weighed_by_unit = request.data.get('is_weighed_by_unit', None)
            unit_of_measure = request.data.get('unit_of_measure', None)

            if is_weighed_by_unit is not None:
                item.is_weighed_by_unit = is_weighed_by_unit

            if is_weighed_by_unit and unit_of_measure:
                item.unit_of_measure = unit_of_measure

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No image URL provided', status=400)

    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return HttpResponse(response.content, content_type=response.headers['Content-Type'])
    except requests.HTTPError as e:
        # If the image URL is incorrect or the image is not accessible
        return HttpResponse('Image not found or access denied', status=e.response.status_code)
    except requests.RequestException as e:
        # For any other exceptions that may occur
        return HttpResponse('An error occurred while fetching the image', status=500)
