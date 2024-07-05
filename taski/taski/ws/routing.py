from django.urls import path
from taski.ws.consumers import NotificationConsumer

websocket_urlpatterns = [
    path(r'ws/notifications/', NotificationConsumer.as_asgi()),
]
