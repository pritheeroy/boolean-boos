from django.urls import path
from .views import ItemView, ItemDetailView, ItemUpdateView

urlpatterns = [
    path('', ItemView.as_view(), name='ItemView'),
    path('detail/', ItemDetailView.as_view(), name='details'),
    path('<uuid:pk>/', ItemUpdateView.as_view()),
]
