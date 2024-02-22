import json
import random

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

from .models import User, Work

DEFAULT_TITLE = 'DjangoDev'


def home(request: HttpRequest):
    data = create_base_data('Home')
    return render(request, 'index.html', data)


def catalog(request: HttpRequest):
    data = create_base_data('Каталог')
    data['workers'] = User.objects.filter(role=2)

    return render(request, 'catalog.html', data)


def show_shorts(request: HttpRequest):
    data = create_base_data('Shorts')
    return render(request, 'shorts.html', data)


def test_method(request: HttpRequest):
    users_data = [
        {'username': 'natalia', 'password': make_password('44444444'), 'role': 2, 'first_name': 'Наталья',
         'last_name': 'Иванова', 'phone_number': '+7 967 949 06 09', 'email': 'natalia@example.com'},
        {'username': 'ivan', 'password': make_password('44444444'), 'role': 2, 'first_name': 'Иван',
         'last_name': 'Петров', 'phone_number': '+7 999 123 45 67', 'email': 'ivan@example.com'},
        {'username': 'elena', 'password': make_password('44444444'), 'role': 2, 'first_name': 'Елена',
         'last_name': 'Сидорова', 'phone_number': '+7 912 345 67 89', 'email': 'elena@example.com'},
        {'username': 'alexey', 'password': make_password('44444444'), 'role': 2, 'first_name': 'Алексей',
         'last_name': 'Козлов', 'phone_number': '+7 999 876 54 32', 'email': 'alexey@example.com'},
        {'username': 'marina', 'password': make_password('44444444'), 'role': 2, 'first_name': 'Марина',
         'last_name': 'Смирнова', 'phone_number': '+7 987 654 32 10', 'email': 'marina@example.com'},
        {'username': 'sergey', 'password': make_password('44444444'), 'role': 2, 'first_name': 'Сергей',
         'last_name': 'Иванов', 'phone_number': '+7 911 987 65 43', 'email': 'sergey@example.com'},
        {'username': 'anna', 'password': make_password('44444444'), 'role': 2, 'first_name': 'Анна',
         'last_name': 'Федорова', 'phone_number': '+7 903 210 98 76', 'email': 'anna@example.com'},
        {'username': 'pavel', 'password': make_password('44444444'), 'role': 2, 'first_name': 'Павел',
         'last_name': 'Морозов', 'phone_number': '+7 922 345 67 89', 'email': 'pavel@example.com'},
        {'username': 'olga', 'password': make_password('44444444'), 'role': 2, 'first_name': 'Ольга',
         'last_name': 'Васильева', 'phone_number': '+7 925 678 90 12', 'email': 'olga@example.com'},
        {'username': 'dmitry', 'password': make_password('44444444'), 'role': 2, 'first_name': 'Дмитрий',
         'last_name': 'Семенов', 'phone_number': '+7 916 543 21 09', 'email': 'dmitry@example.com'},
    ]

    for data in users_data:
        user = User.objects.create(**data)
        Work.objects.create(
            user=user,
            title='Стоматолог-ортопед',
            description='Работа с детьми и взрослыми пациентами. Протезирование зубов и протезирование на имплантах. Диагностика и составление полного плана комплексного стоматологического лечения.',
            address='г. Москва, ул. Ленина 10'
        )
    return JsonResponse({"message": "Выполнено"})


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
