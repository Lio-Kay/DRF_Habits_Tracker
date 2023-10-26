from datetime import datetime
from celery import shared_task
from django.utils import timezone

from habits_app.models import Habit
from utils.TG import send_habit_reminder


@shared_task
def check_habits():
    current_day = datetime.now().weekday()
    habits = Habit.objects.filter(is_pleasant=False)
    for hab in habits:
        user_tg_name = hab.creator.tg_name
        message = (f'Нужно {hab.action}, в {hab.place}, в {hab.time} за {hab.duration}'
                   f'После выполнения вы можете: '
                   f'{hab.related_pleasant_habit.action if hab.related_pleasant_habit.action else hab.reward}')
        if datetime.strptime(hab.created_at, '%A').weekday() == current_day:
            send_habit_reminder(tg_name=user_tg_name, message=message)
        elif hab.frequency == 'DLY':
            send_habit_reminder(tg_name=user_tg_name, message=message)
        elif (hab.frequency == 'WLY' and
              datetime.strptime(hab.created_at, '%A').weekday() == current_day):
            send_habit_reminder(tg_name=user_tg_name, message=message)
        elif (hab.frequency == '2d' and
              (timezone.now().weekday() -
               datetime.strptime(hab.created_at, '%A').weekday()) % 2 == 0):
            send_habit_reminder(tg_name=user_tg_name, message=message)
        elif (hab.frequency == '3d' and
              (timezone.now().weekday() -
               datetime.strptime(hab.created_at, '%A').weekday()) % 3 == 0):
            send_habit_reminder(tg_name=user_tg_name, message=message)
        elif (hab.frequency == '4d' and
              (timezone.now().weekday() -
               datetime.strptime(hab.created_at, '%A').weekday()) % 4 == 0):
            send_habit_reminder(tg_name=user_tg_name, message=message)
        elif (hab.frequency == '5d' and
              (timezone.now().weekday() -
               datetime.strptime(hab.created_at, '%A').weekday()) % 5 == 0):
            send_habit_reminder(tg_name=user_tg_name, message=message)
        elif (hab.frequency == '6d' and
              (timezone.now().weekday() -
               datetime.strptime(hab.created_at, '%A').weekday()) % 6 == 0):
            send_habit_reminder(tg_name=user_tg_name, message=message)
