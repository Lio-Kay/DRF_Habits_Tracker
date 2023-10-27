from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model
from datetime import datetime
import calendar

from habits_app.models import Habit
from habits_app.serializers import HabitSerializer
from habits_app.views import (
    HabitListPersonalCreateAPIView,
    HabitListPublicAPIView,
    HabitRetrieveUpdateDestroyAPIView
)


User = get_user_model()


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password123'
        )

    def test_habit_creation(self):
        habit = Habit.objects.create(
            action='Test Habit',
            time='12:00:00',
            duration=60,
            frequency='DLY',
            created_at='Monday',
            place='Home',
            is_pleasant=True,
            related_pleasant_habit=None,
            reward='Test Reward',
            creator=self.user,
            is_public=True
        )
        self.assertEqual(habit.action, 'Test Habit')
        self.assertEqual(habit.time, '12:00:00')
        self.assertEqual(habit.duration, 60)
        self.assertEqual(habit.frequency, 'DLY')
        self.assertEqual(habit.created_at, 'Monday')
        self.assertEqual(habit.place, 'Home')
        self.assertEqual(habit.is_pleasant, True)
        self.assertEqual(habit.related_pleasant_habit, None)
        self.assertEqual(habit.reward, 'Test Reward')
        self.assertEqual(habit.creator, self.user)
        self.assertEqual(habit.is_public, True)

    def test_habit_string_representation(self):
        habit = Habit.objects.create(
            action='Test Habit',
            time='12:00:00',
            duration=60,
            frequency='DLY',
            created_at='Monday',
            place='Home',
            is_pleasant=True,
            related_pleasant_habit=None,
            reward='Test Reward',
            creator=self.user,
            is_public=True
        )
        expected_string = 'Test Habit, 60, DLY'
        self.assertEqual(str(habit), expected_string)

    def test_habit_verbose_names(self):
        self.assertEqual(
            Habit._meta.verbose_name_plural, 'Привычки'
        )
        self.assertEqual(
            Habit._meta.verbose_name, 'Привычку'
        )

    def test_habit_ordering(self):
        habit1 = Habit.objects.create(
            action='Habit 1',
            time='12:00:00',
            duration=60,
            frequency='DLY',
            created_at='Monday',
            place='Home',
            is_pleasant=True,
            related_pleasant_habit=None,
            reward='Test Reward',
            creator=self.user,
            is_public=True
        )
        habit2 = Habit.objects.create(
            action='Habit 2',
            time='12:00:00',
            duration=60,
            frequency='DLY',
            created_at='Monday',
            place='Home',
            is_pleasant=True,
            related_pleasant_habit=None,
            reward='Test Reward',
            creator=self.user,
            is_public=True
        )
        habits = Habit.objects.all()
        self.assertEqual(habits[0], habit1)
        self.assertEqual(habits[1], habit2)


class HabitListPersonalCreateAPIViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            tg_name='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_create_habit(self):
        request = self.factory.post('habits:habit_list_personal_create', {
            'action': 'Test Habit',
            'time': '12:00:00',
            'duration': 60,
            'place': 'Test Place',
            'is_pleasant': True,
        })
        force_authenticate(request, user=self.user)
        view = HabitListPersonalCreateAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.first().action, 'Test Habit')

    def test_create_habit_with_defaults(self):
        request = self.factory.post('/habits/', {
            'action': 'Test Habit',
            'duration': 1,
            'frequency': 'DLY',
            'place': 'Test Place',
            'is_pleasant': False,
            'reward': 'Test Reward'

        })
        force_authenticate(request, user=self.user)
        view = HabitListPersonalCreateAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 1)
        habit = Habit.objects.first()
        self.assertEqual(habit.action, 'Test Habit')
        current_time = datetime.now().time()
        current_time_str = current_time.strftime('%H:%M:%S.%f')[:-6]  # Remove microseconds
        habit_time_str = habit.time.strftime('%H:%M:%S.%f')[:-6]  # Remove microseconds
        self.assertEqual(current_time_str, habit_time_str)
        self.assertEqual(habit.duration, 1)
        self.assertEqual(habit.frequency, 'DLY')
        self.assertEqual(habit.created_at, calendar.day_name[datetime.now().weekday()])
        self.assertEqual(habit.is_pleasant, False)
        self.assertEqual(habit.reward, 'Test Reward')
        self.assertEqual(habit.creator, self.user)

    def test_get_queryset_superuser(self):
        request = self.factory.get('/habits/')
        force_authenticate(request, user=self.user)
        self.user.is_superuser = True
        self.user.save()
        view = HabitListPersonalCreateAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

    def test_get_queryset_regular_user(self):
        request = self.factory.get('/habits/')
        force_authenticate(request, user=self.user)
        view = HabitListPersonalCreateAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)


class HabitListPublicAPIViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            tg_name='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_get_queryset(self):
        Habit.objects.create(
            action='Test Habit',
            time='12:00:00',
            duration=60,
            frequency='DLY',
            is_public=True,
            reward='Test Reward'
        )
        request = self.factory.get('/habits/')
        force_authenticate(request, user=self.user)
        view = HabitListPublicAPIView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)


class HabitRetrieveUpdateDestroyAPIViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            tg_name='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.habit = Habit.objects.create(
            action='Test Habit',
            time='12:00:00',
            duration=60,
            frequency='DLY',
            place='Test Place',
            reward='Test Reward',
            creator=self.user
        )

    def test_retrieve_habit(self):
        request = self.factory.get(f'/habits/{self.habit.id}/')
        force_authenticate(request, user=self.user)
        view = HabitRetrieveUpdateDestroyAPIView.as_view()
        response = view(request, pk=self.habit.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['action'], 'Test Habit')

    def test_update_habit(self):
        request = self.factory.put(f'/habits/{self.habit.id}/', {
            'action': 'Updated Habit',
            'time': '15:00:00',
            'duration': 90,
            'frequency': 'WLY',
            'place': 'Test Place 2',
            'reward': 'Test Reward 2'
        })
        force_authenticate(request, user=self.user)
        view = HabitRetrieveUpdateDestroyAPIView.as_view()
        response = view(request, pk=self.habit.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Habit.objects.get(id=self.habit.id).action, 'Updated Habit')

    def test_delete_habit(self):
        request = self.factory.delete(f'/habits/{self.habit.id}/')
        force_authenticate(request, user=self.user)
        view = HabitRetrieveUpdateDestroyAPIView.as_view()
        response = view(request, pk=self.habit.id)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Habit.objects.count(), 0)
