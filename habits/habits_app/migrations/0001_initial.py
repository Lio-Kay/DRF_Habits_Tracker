# Generated by Django 4.2.6 on 2023-10-23 18:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=100, verbose_name='Действие')),
                ('time', models.TimeField(blank=True, null=True, verbose_name='Время выполнения')),
                ('duration', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(120)], verbose_name='Время на выполнение в секундах')),
                ('frequency', models.CharField(choices=[('DLY', 'Ежедневно'), ('2d', 'Раз в 2 дня'), ('3d', 'Раз в 3 дня'), ('4d', 'Раз в 4 дня'), ('5d', 'Раз в 5 дней'), ('6d', 'Раз в 6 дней'), ('WLY', 'Еженедельно')], default='DLY', verbose_name='Частота выполнения')),
                ('place', models.CharField(blank=True, max_length=100, null=True, verbose_name='Место выполнения')),
                ('is_pleasant', models.BooleanField(default=False, verbose_name='Признак приятной привычки')),
                ('reward', models.CharField(blank=True, max_length=100, null=True, verbose_name='Вознаграждение за привычку')),
                ('is_public', models.BooleanField(default=False, verbose_name='Признак публичности')),
                ('related_pleasant_habit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='habits_app.habit', verbose_name='Связанная приятная привычка')),
            ],
            options={
                'verbose_name': 'Привычку',
                'verbose_name_plural': 'Привычки',
                'ordering': ('action',),
            },
        ),
    ]