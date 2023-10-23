from rest_framework import generics

from habits_app.models import Habit
from habits_app.serializers import HabitSerializer


class HabitListCreateAPIView(generics.ListCreateAPIView):
    """Вьюсет на создание и вывода списка привычек"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Вьюсет на детальный вывод, редактирование, удаление привычки"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
