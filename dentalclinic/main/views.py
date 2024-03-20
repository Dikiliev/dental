import datetime
import json

from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User, Profile, Appointment, Service, AppointmentService
from .converters import IntListConverter, DateTimeConverter
from .utils import *

DEFAULT_TITLE = 'DentalClinic'


def home(request: HttpRequest):
    data = create_base_data('Home')
    return redirect('/select_specialist/m-1s-1d-1')
    return render(request, 'index.html', data)


def catalog(request: HttpRequest):
    data = create_base_data('Каталог')
    data['workers'] = User.objects.filter(role=2)

    return render(request, 'catalog.html', data)


def select_specialist(request: HttpRequest, specialist_id: int, service_ids: [int], dt: datetime):
    data = create_base_data()
    data['specialist_id'] = specialist_id
    data['service_id'] = service_ids
    data['date'] = dt
    data['workers'] = User.objects.filter(role=2)

    return render(request, 'specialists.html', data)


def select_service(request: HttpRequest, specialist_id: str, service_ids: [int], dt: datetime):
    data = create_base_data()
    data['specialist_id'] = specialist_id
    data['service_id'] = service_ids
    data['date'] = dt

    workers = User.objects.filter(id=specialist_id)

    worker = workers[0] if workers else None
    profile = worker.profile if worker else None
    data['services'] = profile.services.all() if profile else Service.objects.all()

    return render(request, 'services.html', data)


def select_date(request: HttpRequest, specialist_id: int, service_ids: [int], dt: str):
    data = create_base_data()
    data['specialist_id'] = specialist_id
    data['service_id'] = service_ids
    data['date'] = dt

    return render(request, 'select_date.html', data)


def completion_appointment(request: HttpRequest, specialist_id: int, service_ids: [int], dt: str):
    data = create_base_data()

    specialist = User.objects.filter(id=specialist_id)
    if specialist:
        data['specialist'] = specialist[0]

    if type(service_ids) == int:
        service_ids = [service_ids]

    services = Service.objects.filter(id__in=service_ids)

    data['services'] = services
    data['total'] = sum([service.price for service in services])

    dt = DateTimeConverter().to_python(dt)
    data['date'] = {
        'date': dt,
        'day': dt.day,
        'week': get_week(dt),
        'month': get_month(dt),
        'time': dt.strftime('%H:%M')
    }

    data['is_post'] = request.method == 'POST'

    def get(specialist_id: int, service_ids: [int], dt: str):
        return render(request, 'completion_appointment.html', data)

    def post(specialist_id: int, service_ids: [int], dt: str):
        post_data = request.POST

        appointment = Appointment()
        appointment.user = request.user
        appointment.dentist = User.objects.get(id=specialist_id)
        appointment.date_time = dt

        appointment.user_name = post_data.get('name', '')
        appointment.user_phone = post_data.get('phone', '')
        appointment.user_comment = post_data.get('comment', '')

        appointment.save()

        for service_id in service_ids:
            service = Service.objects.get(id=service_id)
            appointment_service = AppointmentService()
            appointment_service.appointment = appointment
            appointment_service.service = service

            appointment_service.save()

        return render(request, 'completion_appointment.html', data)

    if request.method == 'POST':
        return post(specialist_id, service_ids, dt)
    return get(specialist_id, service_ids, dt)


@login_required
def orders(request: HttpRequest):
    data = create_base_data()

    data['orders'] = Appointment.objects.filter(user_id=request.user.id)

    return render(request, 'orders.html', data)


@csrf_exempt
def get_times(request: HttpRequest, specialist_id, year: int, month: int, day: int):
    data = dict()
    data['message'] = 'success'

    dt = datetime(year, month, day)
    specialist = User.objects.get(pk=specialist_id)
    appointments = filter_appointments(dt, specialist.get_appointment_by_list())
    start_time = specialist.profile.start_time
    end_time = specialist.profile.end_time

    times = get_free_times_in_day(dt, appointments, start_time, end_time)

    data['times'] = [t.strftime("%H:%M") for t in times]

    return JsonResponse(data)


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

def test_page(request: HttpRequest, num=12):
    return HttpResponse(f't: {num}')
