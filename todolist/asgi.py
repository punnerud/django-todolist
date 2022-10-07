import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
import lists.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todolist.settings")
django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(lists.routing.websocket_urlpatterns)
        ),
    }
)





