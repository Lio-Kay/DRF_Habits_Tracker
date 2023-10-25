from rest_framework import serializers

from habits_app.models import Habit
from habits_app.validators import IsPleasantConstraint


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = ('id', 'action', 'time', 'duration', 'frequency', 'created_at', 'place',
                  'is_pleasant', 'related_pleasant_habit', 'reward', 'creator', 'is_public',)
        read_only_fields = 'id', 'creator',
        validators = [
            IsPleasantConstraint(
                frequency='frequency',
                created_at='created_at',
                is_pleasant='is_pleasant',
                related_pleasant_habit='related_pleasant_habit',
                reward='reward')
        ]
