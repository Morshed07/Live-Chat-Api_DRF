from rest_framework import serializers
from .models import Message, UserStatus

class UserStatusSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserStatus
        fields = ['user', 'username', 'is_online', 'last_seen']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'content', 'timestamp', 'read']