from django.urls import path
from . import views


SPECIALIST = 'm'
SERVICE = 's'
DATE = 'd'


urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('order/', views.order, name='order'),


    path(f'select_specialist/{SPECIALIST}<specialist_id>{SERVICE}<service_id>{DATE}<date>', views.select_specialist,
         name='select-specialist'),

    path(f'select_service/{SPECIALIST}<specialist_id>{SERVICE}<service_id>{DATE}<date>', views.select_service,
         name='select-service'),

    path(f'select_date/{SPECIALIST}<specialist_id>service<{SERVICE}>{DATE}<date>', views.select_date,
         name='select-date'),

    path(f'completion_appointment/{SPECIALIST}<specialist_id>{SERVICE}<service_id>{DATE}<date>', views.completion_appointment,
         name='completion-appointment'),

    path(f'get_free_times/<specialist_id>', views.get_free_times),

    path('test_page/', views.test_page, name='test-page'),
    path('test_page/<int:num>/', views.test_page, name='test-page'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),


    path('test_method/', views.test_method, name='test-method'),
]
