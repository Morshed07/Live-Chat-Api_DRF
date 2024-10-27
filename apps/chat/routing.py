from django.urls import re_path
from .consumers import StatusConsumer, ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/status/$', StatusConsumer.as_asgi(), name='status'),
    re_path(r'ws/chat/(?P<user_id>\d+)/$', ChatConsumer.as_asgi(), name='chat'),
]