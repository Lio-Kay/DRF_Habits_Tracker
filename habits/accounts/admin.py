from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = 'id', 'email', 'tg_name',
    list_display_links = 'id', 'email', 'tg_name',
    search_fields = 'email',
