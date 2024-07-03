from django.urls import path

from taski.ws.views import WebSocketInfoAPIView

urlpatterns = [
    path('info', WebSocketInfoAPIView.as_view(), name='wsinfo',),
]
