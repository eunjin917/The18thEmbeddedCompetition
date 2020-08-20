from django.contrib import admin
from .models import Register, Accident, User

# Register your models here.

admin.site.register(Register)
# admin.site.register(FileUpload)
admin.site.register(User)
admin.site.register(Accident)