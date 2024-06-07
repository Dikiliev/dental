from .models import *

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm

    fieldsets = (
        (None, {'fields': ('username', 'password', 'new_password', 'confirm_password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )

    def save_model(self, request, obj, form, change):
        obj.set_password(form.cleaned_data.get('new_password'))
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
admin.site.register(Specialization)
admin.site.register(Profile)
admin.site.register(Service)
admin.site.register(Appointment)
admin.site.register(AppointmentService)
admin.site.register(Review)
