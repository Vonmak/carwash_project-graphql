from django.contrib import admin
from .models import User, CarOwner
# from django.apps import apps

class UserA(admin.ModelAdmin):
    list_display = ('email','is_staff','is_car_owner', 'id','first_name', 'last_name','last_login','date_joined','is_superuser','is_verified','otp','otp_expiration',)
    list_filter = ('last_login', 'is_superuser', 'date_joined')
    search_fields = ("first_name__startswith", )
    ordering = ('email',)

admin.site.register(User,UserA)
admin.site.register(CarOwner)