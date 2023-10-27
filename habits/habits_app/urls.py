from django.urls import path

from habits_app.apps import HabitsAppConfig
from habits_app.views import (HabitListPersonalCreateAPIView, HabitListPublicAPIView,
                              HabitRetrieveUpdateDestroyAPIView)

app_name = HabitsAppConfig.name

urlpatterns = [
    path('', HabitListPersonalCreateAPIView.as_view(), name='habit_list_personal_create'),
    path('public/', HabitListPublicAPIView.as_view(), name='habit_list_public_create'),
    path('<int:pk>/', HabitRetrieveUpdateDestroyAPIView.as_view(), name='habit_retrieve_update_destroy'),
]
