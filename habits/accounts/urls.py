from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from accounts.apps import AccountsConfig
from accounts.views import UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView


app_name = AccountsConfig.name

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('', UserListCreateAPIView.as_view(), name='user_list_create'),
    path('<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user_retrieve_update_destroy'),
]
