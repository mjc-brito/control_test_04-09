from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Dados Academicos', {'fields': ('student_number',)}),
    )
    list_display = ('username', 'email', 'student_number', 'is_active')
    search_fields = ('username', 'email', 'student_number')