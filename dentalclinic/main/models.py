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
        (3, 'Менеджер'),
    )

    DEFAULT_AVATAR_URL = 'https://abrakadabra.fun/uploads/posts/2021-12/1640528661_1-abrakadabra-fun-p-serii-chelovek-na-avu-1.png'

    role = models.IntegerField(
        choices=ROLE_ENUM,
        default=1,
        verbose_name='Роль'
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
            return self.DEFAULT_AVATAR_URL

        return self.avatar.url

    def get_appointment_by_list(self):
        appointments = self.dentist_appointments.all()
        return [(appointment.date_time, appointment.get_duration()) for appointment in appointments]

    def get_free_times(self):
        if self.role == 1:
            raise Exception('Попытка получения свободного времени у обычного пользователя')

        profile = self.profile

        if profile is None:
            raise Exception('У специалиста отсутствует специализация (Profile)')

        appointments = self.get_appointment_by_list()

        result = utils.get_free_times(appointments, profile.start_time, profile.end_time)[:6]

        result = {
            'date_str': result[0],
            'times': [{
                'datetime': result[1][i].strftime("%Y-%m-%d-%H-%M"),
                'time_str': result[1][i].strftime("%H:%M")
            } for i in range(min(len(result[1]), 6))],
        }
        return result

    def get_free_times_in_day(self, date):
        if self.role == 1:
            raise Exception('Попытка получения свободного времени у обычного пользователя')

        profile = self.profile

        if profile is None:
            raise Exception('У специалиста отсутствует специализация (Profile)')

        appointments = self.get_appointment_by_list()
        appointments = list(filter(lambda x: x[0].date() == date, appointments))

        result = utils.get_free_times_in_day(date, appointments, profile.start_time, profile.end_time)
        return result

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Specialization(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    specialization = models.ForeignKey(Specialization, default=1, related_name='profiles', on_delete=models.CASCADE, verbose_name='Специализация')
    contact_info = models.TextField(blank=True, verbose_name='Контактная информация')

    description = models.TextField(verbose_name='Краткое портфолио', blank=True)
    address = models.CharField(max_length=150, blank=True, verbose_name='Адрес')

    services = models.ManyToManyField('Service', related_name='profiles', blank=True, verbose_name='Услуги')

    start_time = models.TimeField(default=datetime.time(9, 0), verbose_name='Начало работы')
    end_time = models.TimeField(default=datetime.time(18, 0), verbose_name='Конец работы')

    def __str__(self):
        return f'Профиль {self.user}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Service(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    duration = models.IntegerField(default=60, verbose_name='Продолжительность')
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Appointment(models.Model):
    ORDER_STATUS_CHOICES = (
        (1, 'Создан'),
        (2, 'Принято'),
        (3, 'В процессе'),
        (4, 'Выполнен'),
        (5, 'Отменен'),
    )

    order_number = models.PositiveIntegerField(unique=True,
                                               validators=[MinValueValidator(10000), MaxValueValidator(99999)],
                                               verbose_name='Номер заказа')

    user = models.ForeignKey(User, related_name='user_appointments', on_delete=models.CASCADE, blank=True, default=None, null=True, verbose_name='Пользователь')
    dentist = models.ForeignKey(User, related_name='dentist_appointments', on_delete=models.CASCADE, verbose_name='Врач')
    order_status = models.IntegerField(default=1, choices=ORDER_STATUS_CHOICES, verbose_name='Статус')
    date_time = models.DateTimeField(verbose_name='Дата и время')

    full_name = models.CharField(max_length=150, blank=True, verbose_name='Полное имя')
    user_phone = models.CharField(max_length=25, blank=True, verbose_name='Телефон пользователя')
    user_comment = models.TextField(blank=True, verbose_name='Комментарий пользователя')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Заказ #{self.order_number} на {self.dentist}; {[a.service.title for a in self.appointment_services.all()]} ({self.get_duration()}m)'

    def generate_order_number(self):
        while True:
            order_number = random.randint(10000, 99999)
            if not Appointment.objects.filter(order_number=order_number).exists():
                return order_number

    def get_date_by_str(self):
        return {
            'date': self.date_time,
            'day': self.date_time.day,
            'week': utils.get_week(self.date_time),
            'month': utils.get_month(self.date_time),
            'time': self.date_time.strftime('%H:%M')
        }

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def get_duration(self):
        total = 0

        for appointment in self.appointment_services.all():
            total += appointment.service.duration

        return total

    def get_total_price(self):
        total_price = 0

        for appointment in self.appointment_services.all():
            total_price += appointment.service.price

        return total_price

    def get_avatar_url(self):
        if self.user is None:
            return User.DEFAULT_AVATAR_URL

        return self.user.get_avatar_url()

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class AppointmentService(models.Model):
    appointment = models.ForeignKey(Appointment, related_name='appointment_services', on_delete=models.CASCADE, verbose_name='Запись')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
    quantity = models.IntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.service} x{self.quantity} из {self.appointment}'

    class Meta:
        verbose_name = 'Услуга назначения'
        verbose_name_plural = 'Услуги назначений'


class Review(models.Model):
    dentist = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, verbose_name='Врач')
    author = models.ForeignKey(User, related_name='written_reviews', on_delete=models.CASCADE, verbose_name='Автор')
    rating = models.IntegerField(verbose_name='Рейтинг')
    content = models.TextField(verbose_name='Содержание')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
