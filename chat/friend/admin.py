from django.contrib import admin
from .models import Friends
# Register your models here.
class AdminFriends(admin.ModelAdmin):
    list_display = ['user', 'friend', 'is_active', 'created_at', 'updated_at','msg_group']
    list_editable = ['is_active','msg_group','friend']
    list_filter = ['is_active']
    search_fields = ['user', 'friend']
admin.site.register(Friends)