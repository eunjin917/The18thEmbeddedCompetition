from django.contrib import admin
from .models import Register, FileUpload

# Register your models here.

admin.site.register(Register)
admin.site.register(FileUpload)