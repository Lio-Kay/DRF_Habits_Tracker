# Generated by Django 4.2.6 on 2023-10-25 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='created_at',
            field=models.CharField(blank=True, null=True, verbose_name='День создания'),
        ),
    ]
