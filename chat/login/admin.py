from django.contrib import admin
from login.models import User, UserDetail, Session
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active', 'date_joined']
    list_editable = ['is_staff', 'is_active']
    
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ['user','full_name', 'phone', 'verified']
    list_editable = ['verified']
    
class SessionAdmin(admin.ModelAdmin):
    list_display = ['sessionId', 'token', 'user', 'ip', 'isActive', 'created_at', 'updated_at']
    list_editable = ['isActive']
    
admin.site.register(User, UserAdmin)
admin.site.register(UserDetail, UserDetailAdmin)
admin.site.register(Session, SessionAdmin)