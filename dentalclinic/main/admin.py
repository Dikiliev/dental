from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Work)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(OrderItem)

