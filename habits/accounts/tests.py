from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User
from accounts.serializers import UserSerializer


User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password123',
            tg_name='test_user',
            chat_id=12345,
            last_update=123456789
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.tg_name, 'test_user')
        self.assertEqual(self.user.chat_id, 12345)
        self.assertEqual(self.user.last_update, 123456789)

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), "('test@example.com', 'test_user')")

    def test_user_verbose_name_plural(self):
        self.assertEqual(str(User._meta.verbose_name_plural), "пользователи")

    def test_user_ordering(self):
        self.assertEqual(User._meta.ordering, ('email',))


class UserListCreateAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('accounts:user_list_create')
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        new_user = {
            'email': 'test2@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.url, new_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # Check if a new user is created

    def test_get_user_list(self):
        response = self.client.get(self.url)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_user_list_unauthenticated(self):
        self.client.force_authenticate(user=None)  # Unauthenticate user
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserRetrieveUpdateDestroyAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password123'
        )
        self.url = reverse('accounts:user_retrieve_update_destroy', kwargs={'pk': self.user.pk})
        self.client.force_authenticate(user=self.user)

    def test_get_user(self):
        response = self.client.get(self.url)
        serializer = UserSerializer(self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_user(self):
        updated_data = {
            'email': 'updated@example.com',
            'password': 'newpassword'
        }
        response = self.client.put(self.url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, updated_data['email'])

    def test_delete_user(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
