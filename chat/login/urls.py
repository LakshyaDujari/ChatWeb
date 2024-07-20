
from django.urls import path
from . import views
urlpatterns = [
    path('login_user', views.login_user),
    path('hello/', views.hello_world),
    path('create/', views.create_user),
    path('logout_user/', views.logout_user),
]
