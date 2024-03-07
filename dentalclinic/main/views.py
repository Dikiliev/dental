import datetime
import json
import random

from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

from .models import User, Profile, Appointment, Service
from .converters import IntListConverter, DateTimeConverter
from .utils import *

DEFAULT_TITLE = 'DentalClinic'


def home(request: HttpRequest):
    data = create_base_data('Home')
    return render(request, 'index.html', data)


def catalog(request: HttpRequest):
    data = create_base_data('Каталог')
    data['workers'] = User.objects.filter(role=2)

    return render(request, 'catalog.html', data)


def select_specialist(request: HttpRequest, specialist_id: int, service_ids: [int], date: str):
    data = create_base_data()
    data['specialist_id'] = specialist_id
    data['service_id'] = service_ids
    data['date'] = date

    data['workers'] = User.objects.filter(role=2)

    return render(request, 'specialists.html', data)


def select_service(request: HttpRequest, specialist_id: str, service_ids: [int], date: str):
    data = create_base_data()
    data['specialist_id'] = specialist_id
    data['service_id'] = service_ids
    data['date'] = date

    workers = User.objects.filter(id=specialist_id)

    worker = workers[0] if workers else None
    profile = worker.profile if worker else None
    data['services'] = profile.services.all() if profile else Service.objects.all()

    return render(request, 'services.html', data)


def select_date(request: HttpRequest, specialist_id: int, service_ids: [int], date: str):
    data = create_base_data()
    data['specialist_id'] = specialist_id
    data['service_id'] = service_ids
    data['date'] = date

    return render(request, 'select_date.html', data)


def completion_appointment(request: HttpRequest, specialist_id: int, service_id: int, date: str):
    return HttpResponse(f'specialist: {specialist_id}, service: {service_id}, date: {date}')


def get_free_times(request: HttpRequest, specialist_id: int, day: int = -1):
    appointments = Appointment.objects.all()

    now = datetime.datetime.now()
    current_datetime = datetime.datetime(now.year, now.month, now.day, now.hour, 0, 0)
    if now.minute >= 30:
        current_datetime += datetime.timedelta(hours=1)
    else:
        current_datetime += datetime.timedelta(minutes=30)

    result = []

    for appointment in appointments:
        appointment.date_time = timezone.make_naive(appointment.date_time)

        if appointment.date_time + datetime.timedelta(minutes=appointment.get_duration()) < current_datetime:
            continue

        if appointment.date_time < current_datetime:
            current_datetime = appointment.date_time + datetime.timedelta(minutes=appointment.get_duration())
            continue

        while current_datetime + datetime.timedelta(minutes=30) <= appointment.date_time:
            result.append(current_datetime)
            current_datetime += datetime.timedelta(minutes=30)

        current_datetime += datetime.timedelta(minutes=appointment.get_duration())

    while len(result) < 10:
        result.append(current_datetime)
        current_datetime += datetime.timedelta(minutes=30)

    return HttpResponse(f'message: Success, result: {[str(item.time()) for item in result]}')


def order(request: HttpRequest):
    data = create_base_data('Заказ')

    return render(request, 'order.html', data)


def show_shorts(request: HttpRequest):
    data = create_base_data('Shorts')
    return render(request, 'shorts.html', data)


def test_page(request: HttpRequest, num=12):
    return HttpResponse(f't: {num}')


def test_method(request: HttpRequest):
    name_mappings = {
        'Иван': 'ivan',
        'Александр': 'alexander',
        'Максим': 'maxim',
        'Сергей': 'sergey',
        'Дмитрий': 'dmitry',
        'Елена': 'elena',
        'Ольга': 'olga',
        'Наталья': 'natalia',
        'Анна': 'anna',
        'Мария': 'maria'
    }
    last_name_mappings = {
        'Иванов': 'ivanov',
        'Петров': 'petrov',
        'Сидоров': 'sidorov',
        'Кузнецов': 'kuznetsov',
        'Соколов': 'sokolov',
        'Попова': 'popova',
        'Козлова': 'kozlova',
        'Новикова': 'novikova',
        'Морозова': 'morozova',
        'Волкова': 'volkova'
    }
    professions = ['Стоматолог общей практики', 'Ортодонт', 'Хирург-стоматолог', 'Детский стоматолог', 'Эндодонтист']
    descriptions = [
        'Специалист с богатым опытом в области общей стоматологии, любит работать с детьми и взрослыми.',
        'Эксперт по исправлению прикуса и установке брекетов. Сотни успешных историй улыбок.',
        'Опытный хирург, специализирующийся на сложных операциях в полости рта.',
        'Заботливый подход к лечению детей, создание комфортной и безболезненной атмосферы.',
        'Специалист по лечению корневых каналов с использованием современных технологий.'
    ]
    streets = ['Ленина', 'Мира', 'Советская', 'Молодежная', 'Центральная']

    for i in range(10):
        # Выбор русских имени и фамилии
        first_name = random.choice(list(name_mappings.keys()))
        last_name = random.choice(list(last_name_mappings.keys()))
        # Получение английских аналогов
        first_name_eng = name_mappings[first_name]
        last_name_eng = last_name_mappings[last_name]

        profession = random.choice(professions)
        description = random.choice(descriptions)
        street = random.choice(streets)
        house_number = random.randint(1, 100)
        address = f'ул. {street}, дом {house_number}'

        # Создание уникального username и email на английском

        username = ''
        if random.randint(0, 1) == 0:
            username += f'{first_name_eng[0]}'

        if random.randint(0, 1) == 0 or username == '':
            username += f'{last_name_eng}'

        if random.randint(0, 1) == 0:
            username += f'{random.randint(1, 99)}'

        email = f'{username}@example.com'

        # Создание пользователя
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=make_password('testpassword123'),  # Зашифровать пароль
            role=2
        )
        user.save()

        # Создаем информацию о работе стоматолога
        work = Profile(
            user=user,
            specialization=profession,
            description=description,
            address=address
        )
        work.save()

    return HttpResponse('10 стоматологов с уникальными данными успешно созданы!')


# @csrf_exempt
# def add_comment(request: HttpRequest):
#     if request.method == "POST":
#         data = json.loads(request.body)
#
#         text = data['comment']
#         short = Short.objects.get(id=data['short_id'])
#         user = User.objects.get(id=request.user.id)
#
#         comment = Comment.objects.create(short=short, author=user, text=text)
#         comment.save()
#
#         response_data = {"message": "Данные успешно получены", 'data': data, 'comment': serialize('json', [comment]) }
#         return JsonResponse(response_data)
#     else:
#         return JsonResponse({"error": "Метод запроса должен быть POST"})


@csrf_exempt
def get_times(request: HttpRequest, specialist_id, year: int, month: int, day: int):
    data = dict()
    data['message'] = 'success'

    dt = datetime(year, month, day)
    data['times'] = get_free_times_in_day(dt, [], time(9, 0), time(18, 0))

    return JsonResponse(data)


@csrf_exempt
def get_user(request: HttpRequest, user_id):
    data = dict()

    user = User.objects.get(id=user_id)
    data['user'] = serialize('json', [user])

    return JsonResponse(data)


# @csrf_exempt
# def get_short(request: HttpRequest):
#     shorts = Short.objects.all()
#     short = shorts[random.randint(0, len(shorts) - 1)]
#
#     data = dict()
#     data['short'] = {
#         'id': short.id,
#         'title': short.title,
#         'description': short.description,
#         'url': short.video.url,
#     }
#
#     data['brand'] = serialize('json', [short.brand]),
#     data['comments'] = serialize('json', Comment.objects.filter(short_id=short.id).order_by('-created_at'))
#
#     print(data)
#
#     return JsonResponse(data)


def register(request: HttpRequest):
    data = create_base_data('Регистрация')

    def get():
        return render(request, 'registration/register.html', data)

    def post():
        post_data = request.POST

        user = User()
        user.username = post_data.get('username', '')
        user.phone_number = post_data.get('phone', '')
        user.address = post_data.get('address', '')
        user.role = post_data.get('category', '')

        password = post_data.get('password', '')

        data['username'] = user.username
        data['email'] = user.email

        def check_validate():
            if len(user.username) < 3:
                data['error'] = '* Имя пользователся должно состоять как минимум из 3 симьволов'
                return False

            if user.exist():
                data['error'] = '* Такой пользователь уже существует'
                return False

            if len(password) < 8:
                data['error'] = '* Пароль должен состоять как минимум из 8 симьволов'
                return False
            return True

        if not check_validate():
            return render(request, 'registration/register.html', data)

        user.set_password(password)
        user.save()
        login(request, user)

        return redirect('home')

    if request.method == 'POST':
        return post()
    return get()


def user_login(request: HttpRequest):
    data = create_base_data('Вход')

    def get():
        return render(request, 'registration/login.html')

    def post():
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            return redirect('home')

        data['error'] = '* Неверное имя пользователя или пароль'
        return render(request, 'registration/login.html', data)

    if request.method == 'POST':
        return post()
    return get()


def logout_user(request: HttpRequest):
    logout(request)
    return redirect('login')


# Help functions
def create_base_data(title: str = None):
    if not title:
        title = DEFAULT_TITLE

    return {
        'title': title,
    }
