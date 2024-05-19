from django.contrib import admin
from .models import SharedBoard

# Register your models here.

class SharedBoardAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_group_name', 'get_group_id')

    def get_group_name(self, obj):
        return obj.group.name
    get_group_name.short_description = 'Group Name'

    def get_group_id(self, obj):
        return obj.group.id
    get_group_id.short_description = 'Group ID'

admin.site.register(SharedBoard, SharedBoardAdmin)
