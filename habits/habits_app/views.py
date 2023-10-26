from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from datetime import datetime
import calendar

from habits_app.models import Habit
from habits_app.serializers import HabitSerializer
from habits_app.paginators import HabitPaginator
from habits_app.permissons import IsOwner


class HabitListPersonalCreateAPIView(generics.ListCreateAPIView):
    """Вьюсет на создание и вывод списка персональных привычек"""

    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def perform_create(self, serializer):
        new_habit = serializer.save()
        if new_habit.time is None:
            new_habit.time = datetime.now().time()
        if new_habit.is_pleasant is False:
            current_day = datetime.now().weekday()
            new_habit.created_at = calendar.day_name[current_day]
            if new_habit.frequency is None:
                new_habit.frequency = 'DLY'
        new_habit.creator = self.request.user
        new_habit.save()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Habit.objects.all()
        return Habit.objects.all().filter(creator=user.pk)


class HabitListPublicAPIView(generics.ListAPIView):
    """Вьюсет на вывод списка публичных привычек"""

    queryset = Habit.objects.all().filter(is_public=True)
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator


class HabitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Вьюсет на детальный вывод, редактирование, удаление привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner | IsAdminUser]
