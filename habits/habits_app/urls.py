from django.urls import path
from rest_framework.routers import DefaultRouter

from habits_app.apps import HabitsAppConfig
from habits_app.views import HabitListCreateAPIView, HabitRetrieveUpdateDestroyAPIView

app_name = HabitsAppConfig.name

urlpatterns = [
    path('', HabitListCreateAPIView.as_view(), name='habit_list_create'),
    path('<int:pk>/', HabitRetrieveUpdateDestroyAPIView.as_view(), name='habit_retrieve_update_destroy'),
]
