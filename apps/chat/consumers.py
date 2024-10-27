from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import datetime
from asgiref.sync import sync_to_async
from .models import UserStatus, Message
from apps.users.models import User

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            # Mark user as online
            await self.update_user_status(is_online=True)
            await self.accept()
        else:
            await self.close()  # Reject connection if not authenticated

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            # Mark user as offline and update last_seen
            await self.update_user_status(is_online=False, last_seen=datetime.now())

    async def receive(self, text_data):
        # Placeholder for future features if needed
        pass

    @sync_to_async
    def update_user_status(self, is_online, last_seen=None):
        try:
            status, created = UserStatus.objects.get_or_create(user=self.user)
            status.is_online = is_online
            if last_seen:
                status.last_seen = last_seen
            status.save()
        except Exception as e:
            # Log error
            print(f"Error updating user status: {e}")

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = f"user_{self.user.id}"
        self.room_group_name = self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        if message:
            # Broadcast the message to the group
            await self.send_chat_message(message)

    async def send_chat_message(self, message):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.user.id,
                'sender_username': self.user.username
            }
        )

    async def chat_message(self, event):
        # Receive message from group
        message = event['message']
        sender_id = event['sender_id']
        sender_username = event['sender_username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'sender_username': sender_username
        }))
