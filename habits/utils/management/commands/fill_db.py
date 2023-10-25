import os
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

from habits_app.models import Habit


User = get_user_model()


class Command(BaseCommand):

    help = 'Clear the DB and fills it with data'

    def handle(self, *args, **options):

        User.objects.all().delete()
        Habit.objects.all().delete()

        superuser = User.objects.create_superuser(email=os.getenv('ADMIN_MAIL'),
                                                  tg_name=os.getenv('ADMIN_TELEGRAM_NAME'), password='123')
        user1 = User.objects.create_user(email='abc@mail.com', tg_name=None, password='abc')
        user2 = User.objects.create_superuser(email='def@mail.com', tg_name=None, password='def')

        habit1 = Habit.objects.create(action='Приятная публичная привычка', time="9:30:00",
                                      duration='10', frequency='DLY',
                                      created_at=None, place='Какое-то место',
                                      is_pleasant=True, related_pleasant_habit=None,
                                      reward=None, creator=user1,
                                      is_public=True)
        habit2 = Habit.objects.create(action='Приятная приватная привычка', time="10:30:00",
                                      duration='20', frequency='2d',
                                      created_at=None, place='Какое-то место 2',
                                      is_pleasant=True, related_pleasant_habit=None,
                                      reward=None, creator=user2,
                                      is_public=True)
        habit3 = Habit.objects.create(action='Полезная публичная привычка с приятной публичной привычкой', time="11:30:00",
                                      duration='30', frequency='3d',
                                      created_at=0, place='Какое-то место 3',
                                      is_pleasant=False, related_pleasant_habit=habit1,
                                      reward=None, creator=user1,
                                      is_public=True)
        habit4 = Habit.objects.create(action='Полезная приватная привычка с приятной приватной привычкой', time="12:30:00",
                                      duration='40', frequency='4d',
                                      created_at=1, place='Какое-то место 4',
                                      is_pleasant=False, related_pleasant_habit=habit2,
                                      reward=None, creator=user1,
                                      is_public=False)
        habit5 = Habit.objects.create(action='Полезная публичная привычка с вознаграждением', time="13:30:00",
                                      duration='50', frequency='5d',
                                      created_at=2, place='Какое-то место 5',
                                      is_pleasant=False, related_pleasant_habit=None,
                                      reward='Вознаграждение 1', creator=user2,
                                      is_public=True)
        habit6 = Habit.objects.create(action='Полезная приватная привычка с вознаграждением', time="14:30:00",
                                      duration='60', frequency='6d',
                                      created_at=3, place='Какое-то место 6',
                                      is_pleasant=False, related_pleasant_habit=None,
                                      reward='Вознаграждение 2', creator=user2,
                                      is_public=False)

        self.stdout.write(self.style.SUCCESS('Successfully filled DB'))
