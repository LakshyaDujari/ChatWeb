
from django.urls import path
from . import views
urlpatterns = [
    path('login_user', views.login_user),
    path('create/', views.create_user),
    path('logout_user/', views.logout_user),
    path('get_user_list/', views.get_user_list),
]
