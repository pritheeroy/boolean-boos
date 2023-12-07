from django.urls import path
from .views import ItemView, ItemDetailView, ItemUpdateView, proxy_image

urlpatterns = [
    path('', ItemView.as_view(), name='ItemView'),
    path('detail/', ItemDetailView.as_view(), name='details'),
    path('<uuid:pk>/', ItemUpdateView.as_view()),
    path('proxy_image/', proxy_image, name='proxy_image'),
]
