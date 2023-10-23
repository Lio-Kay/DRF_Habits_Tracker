from django.contrib import admin

from habits_app.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'action', 'time', 'duration', 'frequency', 'place',
                    'is_pleasant', 'related_pleasant_habit', 'reward', 'is_public')
    list_display_links = ('id', 'action', 'place', 'related_pleasant_habit',
                          'reward',)
    list_filter = 'frequency', 'is_pleasant', 'is_public',
    list_editable = 'time', 'duration', 'frequency', 'is_pleasant', 'is_public',
    search_fields = 'action', 'place', 'reward',
