from rest_framework import serializers
from .models import Chat, Message, Status

class ChatSerializer(serializers.ModelSerializer):
    user1_name = serializers.CharField(source="user1.username", read_only=True)
    user2_name= serializers.CharField(source="user2.username", read_only=True)

    class Meta:
        model = Chat
        fields = ["id", "user1", "user1_name", "user2", "user2_name", "last_message", "last_message_time"]

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source = "sender.username", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "chat", "sender", "sender_name", "content", "timestamp"]

class StatusSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username" , read_only=True)

    class Meta:
        model =  Status
        fields = ["id", "user", "user_name", "text", "image", "created_at"]
        read_only_fields = ["id", "user", "created_at"]