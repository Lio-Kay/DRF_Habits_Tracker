from rest_framework import serializers


class IsPleasantConstraint:
    """Проверка полей модели по признакам приятной привычки, полезной привычки и вознаграждения"""
    def __init__(self, frequency, created_at, is_pleasant, related_pleasant_habit, reward):
        self.frequency = frequency
        self.created_at = created_at
        self.is_pleasant = is_pleasant
        self.related_pleasant_habit = related_pleasant_habit
        self.reward = reward

    def __call__(self, value):
        is_pleasant = dict(value).get(self.is_pleasant, '')
        related_pleasant_habit = dict(value).get(self.related_pleasant_habit, '')
        reward = dict(value).get(self.reward, '')
        if is_pleasant:
            if related_pleasant_habit or reward:
                raise serializers.ValidationError(
                    'У приятной привычки не может быть вознаграждения или'
                    ' связанной привычки.')
            if self.frequency:
                raise serializers.ValidationError(
                    'У приятной привычки не может быть частоты выполнения.'
                )
            if self.created_at:
                raise serializers.ValidationError(
                    'У приятной привычки не может быть дня создания.'
                )
        else:
            if related_pleasant_habit and reward:
                raise serializers.ValidationError(
                    'У полезной привычки не может быть вознаграждения и'
                    ' приятной привычки одновременно.')
            if not (related_pleasant_habit or reward):
                raise serializers.ValidationError(
                    'У полезной привычки должно быть вознаграждение либо'
                    ' связанная приятная привычка.')
            if related_pleasant_habit:
                if related_pleasant_habit.is_pleasant is False:
                    raise serializers.ValidationError(
                        'В связанные привычки могут попадать только привычки'
                        ' с признаком приятной привычки.')
