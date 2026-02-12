from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'first_name', 'last_name','password', 'is_staff'),
      }),
    )
    model = User
    list_display = ['id','email', 'first_name', 'last_name', 'password' , 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']

admin.site.register(User, CustomUserAdmin)
