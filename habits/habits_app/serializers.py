from rest_framework import serializers

from habits_app.models import Habit


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = ('id', 'action', 'time', 'duration', 'frequency', 'place',
                  'is_pleasant', 'related_pleasant_habit', 'reward', 'creator', 'is_public',)
        read_only_fields = 'id', 'creator',
