from django.contrib import admin
from .models import Device, Accident, User

# Register your models here.

admin.site.register(Device)
admin.site.register(User)
admin.site.register(Accident)