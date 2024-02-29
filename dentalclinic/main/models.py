import datetime
import random
from . import utils

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
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

    def get_free_times(self):
        if self.role == 1:
            raise Exception('Попытка получения свободного времени у обычного пользователя')

        profile = self.profile
        if profile is None:
            raise Exception('У специалиста отсутвует специализация (Profile)')

        appointments = self.dentist_appointments.all()
        appointments = [(appointment.date_time, appointment.get_duration()) for appointment in appointments]

        result = utils.get_free_times(appointments, profile.start_time, profile.end_time)[:6]

        result = {
            'date_str': result[0],
            'times': [{
                'datetime': result[1][i],
                'time_str': result[1][i].strftime("%H:%M")
            } for i in range(min(len(result[1]), 6))],
        }

        return result


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, blank=True)
    contact_info = models.TextField(blank=True)

    description = models.TextField(verbose_name='Краткое портфолио')
    address = models.CharField(max_length=150, blank=True, verbose_name='Адрес')

    services = models.ManyToManyField('Service', related_name='profiles', blank=True, verbose_name='Услуги')

    start_time = models.TimeField(default=datetime.time(9, 0))
    end_time = models.TimeField(default=datetime.time(18, 0))

    def __str__(self):
        return f'Профиль {self.user}'


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.IntegerField(default=60)
    price = models.IntegerField()

    def __str__(self):
        return self.title


class Appointment(models.Model):
    ORDER_STATUS_CHOICES = (
        (1, 'Создана'),
        (2, 'Принято'),
        (3, 'В процессе'),
        (4, 'Выполнен'),
        (5, 'Отменен'),
    )

    order_number = models.PositiveIntegerField(unique=True,
                                               validators=[MinValueValidator(10000), MaxValueValidator(99999), ],
                                               verbose_name='Номер заказа')

    user = models.ForeignKey(User, related_name='user_appointments', on_delete=models.CASCADE)
    dentist = models.ForeignKey(User, related_name='dentist_appointments', on_delete=models.CASCADE)
    order_status = models.IntegerField(default=1, choices=ORDER_STATUS_CHOICES, verbose_name='Статус')
    date_time = models.DateTimeField()

    def __str__(self):
        return f'Заказ #{self.order_number}; {[a.service.title for a in self.appointments.all()]} ({self.get_duration()}m)'

    def generate_order_number(self):
        while True:
            order_number = random.randint(10000, 99999)
            if not Appointment.objects.filter(order_number=order_number).exists():
                return order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def get_duration(self):
        total = 0

        for appointment in self.appointments.all():
            total += appointment.service.duration

        return total


class AppointmentService(models.Model):
    appointment = models.ForeignKey(Appointment, related_name='appointments', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.service} x{self.quantity} из {self.appointment}'


class Review(models.Model):
    dentist = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='written_reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    content = models.TextField()
