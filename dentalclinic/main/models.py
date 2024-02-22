import datetime
import random

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_ENUM = (
        (1, 'Пользователь'),
        (2, 'Врач'),
    )

    role = models.IntegerField(
        choices=ROLE_ENUM,
        default=1
    )

    avatar = models.ImageField(blank=True, verbose_name='Аватарка')
    phone_number = models.CharField(max_length=25, blank=True, verbose_name='Номер телефона')

    def __str__(self):
        return self.username

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    def exist(self):
        return len(User.objects.filter(username=self.username)) > 0

    def get_avatar_url(self):
        if not self.avatar:
            return 'https://abrakadabra.fun/uploads/posts/2021-12/1640528661_1-abrakadabra-fun-p-serii-chelovek-na-avu-1.png'

        return self.avatar.url


class Work(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='Работник')

    title = models.CharField(max_length=150, verbose_name='Профессия')
    description = models.TextField(verbose_name='Краткое портфолио')

    address = models.CharField(max_length=150, blank=True, verbose_name='Адрес')
