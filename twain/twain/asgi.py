"""
ASGI config for twain project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digibuddies.settings')
import django
django.setup()

application = ProtocolTypeRouter({
  'http': django_asgi_app,
  'websocket': AuthMiddlewareStack(  # new
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})