from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/chat/<str:group_name>/<str:user_name>/', ChatConsumer.as_asgi()),
    # path('ws/notification/', NotificationConsumer.as_asgi())
]