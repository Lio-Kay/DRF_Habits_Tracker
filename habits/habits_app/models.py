from django.db import models
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError

from habits_app.apps import HabitsAppConfig

app_name = HabitsAppConfig.name

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    """Модель привычки"""
    action = models.CharField(max_length=100,
                              verbose_name='Действие')
    time = models.TimeField(**NULLABLE,
                            verbose_name='Время выполнения')
    duration = models.PositiveSmallIntegerField(validators=[MaxValueValidator(120)],
                                                verbose_name='Время на выполнение в секундах')
    frequency_choices = [
        ('DLY', 'Ежедневно'),
        ('2d', 'Раз в 2 дня'),
        ('3d', 'Раз в 3 дня'),
        ('4d', 'Раз в 4 дня'),
        ('5d', 'Раз в 5 дней'),
        ('6d', 'Раз в 6 дней'),
        ('WLY', 'Еженедельно'),
    ]
    frequency = models.CharField(default='DLY', choices=frequency_choices,
                                 verbose_name='Частота выполнения')
    place = models.CharField(**NULLABLE, max_length=100,
                             verbose_name='Место выполнения')
    is_pleasant = models.BooleanField(default=False,
                                      verbose_name='Признак приятной привычки')
    related_pleasant_habit = models.ForeignKey(**NULLABLE, to='self', on_delete=models.SET_NULL,
                                               verbose_name='Связанная приятная привычка')
    reward = models.CharField(**NULLABLE, max_length=100,
                              verbose_name='Вознаграждение за привычку')

    # creator = models.ManyToManyField(**NULLABLE, to=,verbose_name='Создатель привычки')
    is_public = models.BooleanField(default=False,
                                    verbose_name='Признак публичности')

    def __str__(self):
        return f'''{self.action}, {self.duration}, {self.frequency},
        {(self.related_pleasant_habit if self.related_pleasant_habit else self.reward)
        if not self.is_pleasant else None}'''

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = 'action',

    def clean(self):
        super().clean()
        if self.is_pleasant:
            if self.reward or self.related_pleasant_habit:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения "
                    "или связанной привычки.")
        else:
            if not self.related_pleasant_habit and not self.reward:
                raise ValidationError(
                    "У полезной привычки должно быть вознаграждение"
                    " либо связанная приятная привычка.")
            if self.related_pleasant_habit and self.reward:
                raise ValidationError(
                    "У полезной привычки не может быть одновременно и "
                    "вознаграждение и связанная приятная привычка")
            if self.related_pleasant_habit:
                if self.related_pleasant_habit.is_pleasant is False:
                    raise ValidationError(
                        "В связанные привычки могут попадать только "
                        "привычки с признаком приятной привычки.")
