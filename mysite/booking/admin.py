from django.contrib import admin

from .models import Property, CustomUser
# Register your models here.
admin.site.register(Property)
admin.site.register(CustomUser)
