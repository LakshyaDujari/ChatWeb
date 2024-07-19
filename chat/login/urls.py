
from django.urls import path
from . import views
urlpatterns = [
    path('access/', views.login_user),
    path('hello/', views.hello_world),
]
