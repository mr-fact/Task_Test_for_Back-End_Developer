from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView


class WebSocketInfoAPIView(
    APIView
):
    @extend_schema(
        tags=['WebSocket'],
        summary='web socket connection info',
        description='WebSocket connection established at ws://localhost:8000/ws/myapp/',
    )
    def get(self, request):
        return Response({"info": "WebSocket connection established at ws://localhost:8000/ws/myapp/"})
