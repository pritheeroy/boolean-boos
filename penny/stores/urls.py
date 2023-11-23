from django.urls import path
from .views import StoreView, StoreItemView, get_stores_distance

urlpatterns = [
    path('', StoreView.as_view(), name='store-view'),
    # path('<int:pk>/',
    #      ItemUpdateView.as_view(), name='item-update'),
    path('<int:pk>/', StoreItemView.as_view()),
    path('distance/', get_stores_distance, name='get_stores_distance')
]
