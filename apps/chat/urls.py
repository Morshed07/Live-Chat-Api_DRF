from django.urls import path
from .views import UserStatusListAPIView, MessageHistoryAPIView, SendMessageView

urlpatterns = [
    path('user-status/', UserStatusListAPIView.as_view(), name='user-status-list'),
    path('message-history/<int:user_id>/', MessageHistoryAPIView.as_view(), name='message-history'),
    path('send-message/', SendMessageView.as_view(), name='send-message'),
]