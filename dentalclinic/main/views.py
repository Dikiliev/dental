import datetime
import json

from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template import engines
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import *
from .converters import IntListConverter, DateTimeConverter
from .utils import *

DEFAULT_TITLE = 'ЛДент Стоматологическа клиника'


def home(request: HttpRequest):
    # if not request.user.is_authenticated:
    #     return redirect('login')

    context = create_base_data(request)
    return render(request, 'index.html', context)
    return redirect('/select_specialist/m-1s-1d-1')


def select_specialist(request: HttpRequest, specialist_id: int, service_ids: [int], dt: datetime):
    data = create_base_data(request)
    data['specialist_id'] = specialist_id
    data['service_id'] = service_ids
    data['date'] = dt

    workers_query = User.objects.filter(role=2)

    if service_ids and service_ids != -1 and service_ids[0] != -1:
        workers_query = workers_query.filter(
            profile__services__id__in=service_ids
        ).annotate(
            services_count=Count('profile__services', distinct=True)
        ).filter(
            services_count=len(service_ids)
        )
    else:
        workers_query = workers_query.annotate(
            services_count=Count('profile__services')
        ).filter(
            services_count__gt=0
        )

    data['workers'] = workers_query

    return render(request, 'specialists.html', data)


def select_service(request: HttpRequest, specialist_id: str, service_ids: [int], dt: datetime):
    data = create_base_data(request)
    data['specialist_id'] = specialist_id
    data['service_id'] = service_ids
    data['date'] = dt

    workers = User.objects.filter(id=specialist_id)

    worker = workers[0] if workers else None
    profile = worker.profile if worker else None
    data['services'] = profile.services.all() if profile else Service.objects.all()

    return render(request, 'services.html', data)


def select_date(request: HttpRequest, specialist_id: int, service_ids: [int], dt: str):
    data = create_base_data(request)
    data['specialist_id'] = specialist_id
    data['service_id'] = service_ids
    data['date'] = dt

    return render(request, 'select_date.html', data)


def completion_appointment(request: HttpRequest, specialist_id: int, service_ids: [int], dt: str):
    data = create_base_data(request)

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

        appointment.dentist = User.objects.get(id=specialist_id)

        if request.user.is_authenticated:
            appointment.user = request.user

        appointment.date_time = dt

        appointment.full_name = post_data.get('full_name', '')
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


def edit_date(request: HttpRequest, order_id: int):
    data = create_base_data(request)
    order = Appointment.objects.get(id=order_id)

    data['specialist_id'] = order.dentist_id
    data['service_id'] = [service.id for service in order.appointment_services.all()]
    data['date'] = order.date_time

    data['is_edit_date'] = True
    data['order_id'] = order_id

    return render(request, 'select_date.html', data)


@login_required
def orders(request: HttpRequest):
    data = create_base_data(request)

    if request.user.role == 3:
        data['orders'] = Appointment.objects.filter(date_time__gte=datetime.today()).order_by('-create_date')
        return render(request, 'manager/orders.html', data)

    if request.user.role == 1:
        data['orders'] = Appointment.objects.filter(user_id=request.user.id).order_by('-create_date')
    else:
        data['orders'] = Appointment.objects.filter(dentist_id=request.user.id).order_by('-create_date')

    return render(request, 'orders.html', data)


@login_required
def profile_edits(request: HttpRequest):
    data = create_base_data(request, )

    user = request.user

    data['specializations'] = Specialization.objects.all()
    data['services'] = Service.objects.all()
    data['selected_services'] = user.profile.services.all()

    def get():
        return render(request, 'profile.html', data)

    def post():
        post_data = request.POST
        uploaded_image = request.FILES.get('image_file', None)

        if uploaded_image:
            user.avatar = uploaded_image

        services = Service.objects.filter(title__in=post_data.getlist('services', []))
        user.profile.services.set(services)

        user.phone_number = post_data.get('phone', '')
        user.profile.specialization = Specialization.objects.get(id=post_data.get('specialization', ''))
        user.profile.description = post_data.get('description', '')

        user.profile.save()
        user.save()

        data['message'] = 'Сохранено!'

        return render(request, 'profile.html', data)

    if request.method == 'POST':
        return post()

    return get()


def get_times(request: HttpRequest, specialist_id, year: int, month: int, day: int):
    data = dict()
    data['message'] = 'success'

    dt = datetime(year, month, day).date()
    specialist = User.objects.get(pk=specialist_id)
    appointments = filter_appointments(dt, specialist.get_appointment_by_list())
    start_time = specialist.profile.start_time
    end_time = specialist.profile.end_time

    times = get_free_times_in_day(dt, appointments, start_time, end_time)

    data['times'] = [t.strftime("%H:%M") for t in times]

    return JsonResponse(data)


@login_required()
def set_order_status(request: HttpRequest):
    try:
        data = json.loads(request.body)
        order = Appointment.objects.get(id=data['id'])
        order.order_status = data['value']
        order.save()
        return JsonResponse({'message': 'success'})
    except Exception as err:
        print(f'ERROR: {err}')
        return JsonResponse({'message': err})


def set_order_date(request: HttpRequest):
    try:
        data = json.loads(request.body)

        dt = DateTimeConverter().to_python( data['value'])

        order = Appointment.objects.get(id=data['id'])
        order.date_time = dt
        order.save()
        return JsonResponse({'message': 'success'})
    except Exception as err:
        print(f'ERROR: {err}')
        return JsonResponse({'message': err})


def shel_command(request: HttpRequest):
    return JsonResponse({"message": 'success'})


def manager_main(request: HttpRequest):
    context = create_base_data(request)
    context['orders'] = Appointment.objects.filter(date_time__gte=datetime.today()).order_by('date_time')[:5]
    return render(request, 'manager/main.html', context)


def create_specialist(request: HttpRequest):
    context = create_base_data(request)
    context['username'] = ''
    context['email'] = ''
    context['first_name'] = ''
    context['last_name'] = ''
    context['phone'] = ''

    def get():
        return render(request, 'manager/create_specialist.html', context)

    def post():
        post_data = request.POST

        user = User()
        user.username = post_data.get('username', '')
        user.first_name = post_data.get('first_name', '')
        user.last_name = post_data.get('last_name', '')
        user.phone_number = post_data.get('phone', '')
        user.address = post_data.get('address', '')
        user.role = 2

        password = post_data.get('password', '')

        context['username'] = user.username
        context['email'] = user.email
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        context['phone'] = user.phone_number

        def check_validate():
            if len(user.username) < 3:
                context['error'] = '* Имя пользователся должно состоять как минимум из 3 симьволов'
                return False

            if user.exist():
                context['error'] = '* Такой пользователь уже существует'
                return False

            if len(password) < 8:
                context['error'] = '* Пароль должен состоять как минимум из 8 симьволов'
                return False
            return True

        if not check_validate():
            return render(request, 'manager/create_specialist.html', context)

        user.set_password(password)
        user.save()

        profile = Profile(user=user)
        profile.save()

        context['specialist'] = user
        context['password'] = password
        return render(request, 'manager/specialist_created.html', context)

    if request.method == 'POST':
        return post()
    return get()


def create_order(request: HttpRequest):
    context = create_base_data(request)
    context['orders'] = Appointment.objects.filter(date_time__gte=datetime.today()).order_by('date_time')[:5]
    return render(request, 'manager/create_order.html', context)


def register(request: HttpRequest):
    context = create_base_data(request,)
    context['username'] = ''
    context['email'] = ''
    context['first_name'] = ''
    context['last_name'] = ''
    context['phone'] = ''

    def get():
        print(context)
        return render(request, 'registration/register.html', context)

    def post():
        post_data = request.POST

        user = User()
        user.username = post_data.get('username', '')
        user.first_name = post_data.get('first_name', '')
        user.last_name = post_data.get('last_name', '')
        user.phone_number = post_data.get('phone', '')
        user.address = post_data.get('address', '')
        user.role = 1

        password = post_data.get('password', '')

        context['username'] = user.username
        context['email'] = user.email
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        context['phone'] = user.phone_number

        def check_validate():
            if len(user.username) < 3:
                context['error'] = '* Имя пользователся должно состоять как минимум из 3 симьволов'
                return False

            if user.exist():
                context['error'] = '* Такой пользователь уже существует'
                return False

            if len(password) < 8:
                context['error'] = '* Пароль должен состоять как минимум из 8 симьволов'
                return False
            return True

        if not check_validate():
            return render(request, 'registration/register.html', context)

        user.set_password(password)
        user.save()
        login(request, user)

        if user.role == 2:
            profile = Profile(user=user)
            profile.save()
            return redirect('profile')

        return redirect('home')

    if request.method == 'POST':
        return post()
    return get()


def user_login(request: HttpRequest):
    data = create_base_data(request)

    def get():

        # jinja2_engine = engines['jinja2']
        # template = jinja2_engine.get_template('registration/login.html')
        # rendered_template = template.render(data)
        # return HttpResponse(rendered_template)

        return render(request, 'registration/login.html', data)

    def post():
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        data['username'] = request.POST['username']

        if user is not None:
            login(request, user)

            if user.role == 1:
                return redirect('home')

            return redirect('orders')

        data['error'] = '* Неверное имя пользователя или пароль'

        return render(request, 'registration/login.html', data)

    if request.method == 'POST':
        return post()
    return get()


def logout_user(request: HttpRequest):
    logout(request)
    return redirect('login')


# Help functions
def create_base_data(request: HttpRequest, title: str = None):
    if not title:
        title = DEFAULT_TITLE

    return {
        'user': request.user,
        'title': title,
    }

