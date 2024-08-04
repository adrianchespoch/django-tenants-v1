from django.contrib import admin

# Register your models here.
from .models import User, ExtendedGroup

admin.site.register(User)
admin.site.register(ExtendedGroup)

