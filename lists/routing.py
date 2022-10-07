from .consumers import TodoListConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r"ws/(?P<room_name>\w+)/$", TodoListConsumer.as_asgi()),
]
