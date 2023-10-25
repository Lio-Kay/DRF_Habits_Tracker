from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


NULLABLE = {'blank': True, 'null': True}


class CustomUserManager(BaseUserManager):
    """Кастомная модель для создания пользователя"""

    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    """Кастомная модель пользователя"""

    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    tg_name = models.CharField(**NULLABLE, unique=True, max_length=50, verbose_name='Telegram аккаунт')
    chat_id = models.PositiveIntegerField(**NULLABLE, verbose_name='ID чата ТГ')
    last_update = models.PositiveBigIntegerField(**NULLABLE, verbose_name='ID последнего сообщения')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email, self.tg_name}'

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'
        ordering = 'email',
