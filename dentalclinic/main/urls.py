from django.urls import path, register_converter
from . import views, converters


SPECIALIST = 'm'
SERVICE = 's'
DATE = 'd'

register_converter(converters.IntListConverter, 'intlist')
register_converter(converters.DateTimeConverter, 'datetime')


urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
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

    path(f'get_times/<int:specialist_id>/<int:year>/<int:month>/<int:day>', views.get_times, name='get-times'),
    path(f'set_order_status/', views.set_order_status, name='get-times'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),


    path('shell_command/', views.shel_command, name='shel_command'),
    # path('test_method/', views.test_method, name='test-method'),
]
