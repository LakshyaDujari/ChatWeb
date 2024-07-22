from django.urls import path
from . import views

urlpatterns = [
    path('chatwindow/', views.get_group_chat),
    path('sendmsg/', views.send_msg2grp),
    path('get_all_groups/', views.get_all_msg_groups),
]
