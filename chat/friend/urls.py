from django.urls import path
from . import views

urlpatterns = [
    path('add_friend/', views.add_friend),
    path('get_friend/', views.get_friend),
    path('get_friend_request/', views.get_friend_request),
    path('accept_friend_request/', views.accept_friend_request),
    path('reject_friend_request/', views.reject_friend_request),
    path('unfriend/', views.unfriend),
    path('get_all_friends/', views.get_all_friends),
    path('search_friend/', views.get_user),
    path('get_all_users/', views.get_all_users),
]
