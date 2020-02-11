from django.contrib import admin
from pv.models import  user_type, Pv


# Register your models here.

admin.site.register(Pv)
admin.site.register(user_type)
