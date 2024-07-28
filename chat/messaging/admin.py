from django.contrib import admin
from .models import MessageGroup,Message
# Register your models here.
# class MessageGroupAdmin(admin.ModelAdmin):
#     list_display = ('id', 'GroupName', 'Member')
#     search_fields = ('name',)
    
# class MessageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'Group', 'Author', 'Body', 'Timestamp')
#     search_fields = ('group',)
    
admin.site.register(MessageGroup)
admin.site.register(Message)