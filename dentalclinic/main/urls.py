from django.urls import path, register_converter
from . import views, converters


SPECIALIST = 'm'
SERVICE = 's'
DATE = 'd'

register_converter(converters.IntListConverter, 'intlist')
register_converter(converters.DateTimeConverter, 'datetime')


urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', views.orders, name='orders'),
    path('profile/', views.profile_edits, name='profile'),

    path(f'select_specialist/{SPECIALIST}<specialist_id>{SERVICE}<intlist:service_ids>{DATE}<dt>', views.select_specialist,
         name='select-specialist'),

    path(f'select_service/{SPECIALIST}<specialist_id>{SERVICE}<intlist:service_ids>{DATE}<dt>', views.select_service,
         name='select-service'),

    path(f'select_date/{SPECIALIST}<specialist_id>{SERVICE}<intlist:service_ids>{DATE}<dt>', views.select_date,
         name='select-date'),

    path(f'completion_appointment/{SPECIALIST}<specialist_id>{SERVICE}<intlist:service_ids>{DATE}<dt>', views.completion_appointment,
         name='completion-appointment'),

    path(f'edit_date/<int:order_id>', views.edit_date,
         name='edit-date'),

    path(f'get_times/<int:specialist_id>/<int:year>/<int:month>/<int:day>', views.get_times, name='get-times'),
    path(f'set_order_status/', views.set_order_status, name='set-order-status'),
    path(f'set_order_date/', views.set_order_date, name='set-order-date'),

    path(f'manager/main', views.manager_main, name='manager_main'),
    path(f'manager/create_specialist', views.create_specialist, name='manager_create_specialist'),
    path(f'manager/create_order', views.create_order, name='create_order'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),


    path('shell_command/', views.shel_command, name='shel_command'),
    # path('test_method/', views.test_method, name='test-method'),
]
