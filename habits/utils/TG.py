import os
import requests
from django.contrib.auth import get_user_model


User = get_user_model()
token = os.getenv('TELEGRAM_API')


def get_updates(last_update):
    return requests.get(url=f'https://api.telegram.org/bot{token}/getUpdates?offset={last_update+1}').json()


def save_updated_data(updates_result):
    for update in updates_result:
        user = User.objects.get(tg_name=update.get('message').get('chat').get('username'))
        if User.objects.filter(tg_name=user).exists():
            user.chat_id = update.get('message').get('chat').get('id')
            user.last_update = update.get('update_id')
            user.save()


def send_habit_reminder(tg_name, message):
    last_update = User.objects.latest('chat_id').chat_id
    updates = get_updates(last_update)
    if updates.get('ok'):
        save_updated_data(updates.get('result'))

    chat_id = User.objects.get(tg_name=tg_name).chat_id
    if chat_id is False:
        print('Error. Can\'t find user\'s chat ID')
        return
    data = {
        'chat_id': chat_id,
        'text': message,
    }
    return requests.get(url=f'https://api.telegram.org/bot{token}/sendMessage', params=data)
