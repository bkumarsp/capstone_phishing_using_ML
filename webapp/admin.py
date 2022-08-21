from django.contrib import admin
from .models import AppUserModel

# Register your models here.

@admin.register(AppUserModel)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AppUserModel._meta.get_fields()]