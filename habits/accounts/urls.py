from django.urls import path

from accounts.apps import AccountsConfig
from accounts.views import UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView


app_name = AccountsConfig.name

urlpatterns = [
    path('', UserListCreateAPIView.as_view(), name='user_list_create'),
    path('<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user_retrieve_update_destroy'),
]
