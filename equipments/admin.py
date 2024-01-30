from django.contrib import admin

# Register your models here.
from .models import Equipment, Production

admin.site.register(Equipment)
admin.site.register(Production)
