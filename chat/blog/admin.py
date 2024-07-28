from django.contrib import admin
from blog.models import Blog
# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'user', 'img_path' ,'created_at', 'updated_at']
    list_editable = ['user','title', 'content', 'user', 'img_path']
    list_display_links = ['created_at']
    
admin.site.register(Blog, BlogAdmin)
    