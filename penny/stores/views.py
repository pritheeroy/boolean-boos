from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Item
from stores.models import Store
from .serializers import StoreSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status
from django.conf import settings
import requests

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10


class StoreView(ListAPIView):
    serializer_class = StoreSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name']  # Search by name or store
    permission_classes = [AllowAny]

    def get_queryset(self):
        search_term = self.request.query_params.get('name')
        queryset = Store.objects.all()

        # Filter by name if a search term is provided
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)

        return queryset


class StoreItemView(ListAPIView):
    serializer_class = StoreSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Retrieve the store based on the 'pk' parameter from the URL
        # assuming the URL parameter is named 'pk'
        store_id = self.kwargs.get('pk')
        store = get_object_or_404(Store, pk=store_id)

        # Return the items associated with the store
        queryset = store.items.all()
        return queryset
    
def get_stores_distance(request):
    user_location = request.GET.get('user_location')
    google_api_key = 'AIzaSyDpIWKiBj1P0x5buBX2losmBknSRYn1HVI'

    # Supabase REST URL and Headers
    supabase_url = 'https://ytjttwkyfkltqqxpdaox.supabase.co/rest/v1/stores_store'
    supabase_headers = {
        'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl0anR0d2t5ZmtsdHFxeHBkYW94Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDA1MzA2NDQsImV4cCI6MjAxNjEwNjY0NH0.BJxaaSqeCJDp2vKOMj2UNW5YwytqezaLfez24kPMuZs',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl0anR0d2t5ZmtsdHFxeHBkYW94Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDA1MzA2NDQsImV4cCI6MjAxNjEwNjY0NH0.BJxaaSqeCJDp2vKOMj2UNW5YwytqezaLfez24kPMuZs'
    }

    # Fetch stores from Supabase
    stores_response = requests.get(supabase_url, headers=supabase_headers)
    if stores_response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch data from Supabase'}, status=500)

    stores = stores_response.json()
    destinations = '|'.join([store['location'] for store in stores])

    # Google Maps API to calculate distances
    maps_response = requests.get(
        'https://maps.googleapis.com/maps/api/distancematrix/json',
        params={
            'origins': user_location,
            'destinations': destinations,
            'key': google_api_key
        }
    )

    if maps_response.status_code == 200:
        elements = maps_response.json().get('rows', [])[0].get('elements', [])
        store_distances = []
        for store, element in zip(stores, elements):
            if element['status'] == 'OK':
                distance_text = element['distance']['text']
                store_distances.append({
                    'name': store['name'],
                    'distance': distance_text
                })
        print(store_distances)
        return JsonResponse(store_distances, safe=False)
    else:
        return JsonResponse({'error': 'Failed to fetch distances'}, status=500)
