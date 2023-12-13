from django.contrib.auth.models import AbstractUser
from django.db import models

from education.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')  # Этой строкой делаем поле уникальным.

    first_name = models.CharField(max_length=30, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=40, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []