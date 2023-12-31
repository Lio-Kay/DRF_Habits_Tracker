# Generated by Django 4.2.6 on 2023-10-26 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('habits_app', '0004_remove_habit_only_useful_habit_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='habit', to=settings.AUTH_USER_MODEL, verbose_name='Создатель привычки'),
        ),
    ]
