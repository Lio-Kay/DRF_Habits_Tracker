from django.contrib import admin

from habits_app.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'action', 'time', 'duration', 'frequency',
                    'created_at', 'is_pleasant', 'is_public',)
    list_display_links = ('id', 'action',)
    list_filter = 'frequency', 'is_pleasant', 'is_public',
    list_editable = ('time', 'duration', 'frequency', 'created_at',
                     'is_pleasant', 'is_public',)
    search_fields = 'action', 'place', 'reward',
