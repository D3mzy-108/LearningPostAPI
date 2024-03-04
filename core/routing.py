from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from challenge_app.consumers import WaitingRoom

websocket_urlpatterns = [
    path("challenge/<str:room_name>/waiting_room/",
         WaitingRoom.as_asgi()),
    # MORE PATHS GO HERE
]
