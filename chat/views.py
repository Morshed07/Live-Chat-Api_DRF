# from rest_framework.views import APIView
# from rest_framework import generics
# from rest_framework.response import Response
# from asgiref.sync import async_to_sync
# from rest_framework.permissions import IsAuthenticated
# from channels.layers import get_channel_layer
# from .models import UserStatus, Message
# from .serializers import UserStatusSerializer, MessageSerializer
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from django.conf import settings  

# class UserStatusListAPIView(generics.ListAPIView):
#     serializer_class = UserStatusSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         # Assuming you have a way to identify the user's friends
#         friends = user.friends.all()  # Replace with your actual friends list query
#         return UserStatus.objects.filter(user__in=friends)

# class MessageHistoryAPIView(generics.ListAPIView):
#     serializer_class = MessageSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         other_user_id = self.kwargs['user_id']
#         get_object_or_404(settings.AUTH_USER_MODEL, id=other_user_id)  # Ensure the user exists
#         return Message.objects.filter(
#             sender_id__in=[user.id, other_user_id],
#             receiver_id__in=[user.id, other_user_id]
#         ).order_by('timestamp')

# class SendMessageView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         receiver_id = request.data.get('receiver_id')
#         message = request.data.get('message')

#         # Validate input data
#         if not receiver_id or not message:
#             return Response({"error": "Receiver ID and message content are required."}, status=status.HTTP_400_BAD_REQUEST)

#         if receiver_id == request.user.id:
#             return Response({"error": "You cannot send a message to yourself."}, status=status.HTTP_400_BAD_REQUEST)

#         # Ensure the receiver exists
#         receiver = get_object_or_404(settings.AUTH_USER_MODEL, id=receiver_id)

#         # Get the channel layer
#         channel_layer = get_channel_layer()
        
#         # Send message to the receiver's group
#         try:
#             async_to_sync(channel_layer.group_send)(
#                 f"user_{receiver_id}",  # Unique group name for the user
#                 {
#                     'type': 'chat_message',
#                     'message': message,
#                     'sender_id': request.user.id,
#                     'sender_username': request.user.username,
#                 }
#             )
#             return Response({"status": "Message sent"})
#         except Exception as e:
#             return Response({"error": f"Failed to send message: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.shortcuts import render

def room(request, room_name):
    return render(request, 'chat/chat.html', {
        'room_name': room_name
    })
