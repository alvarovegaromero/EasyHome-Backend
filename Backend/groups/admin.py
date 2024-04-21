from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Group, UserGroup

admin.site.register(Group)
admin.site.register(UserGroup)