import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from channels.auth import AuthMiddlewareStack
import chatting.routing  # 채팅 앱 이름

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'popin.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),

    "websocket": SessionMiddlewareStack(
        AuthMiddlewareStack(
            URLRouter(
                chatting.routing.websocket_urlpatterns
            )
        )
    ),
})