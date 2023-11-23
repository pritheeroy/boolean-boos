from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.CreateAccountView.as_view(), name='signup'),
    path('update/', views.UpdateAccountView.as_view(),
         name='update-account'),
    path('info/', views.AccountInfoView.as_view(), name='account-info'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
