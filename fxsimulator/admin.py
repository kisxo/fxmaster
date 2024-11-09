from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Order

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'balance', 'first_name', 'last_name', 'is_staff']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Order)