from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path('create/', views.create_blog),
    path('get/', views.get_blog),
    path('update/', views.update_blog),
    path('delete/', views.delete_blog),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
