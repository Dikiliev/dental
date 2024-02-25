from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Service)
admin.site.register(Appointment)
admin.site.register(AppointmentService)
admin.site.register(Review)

