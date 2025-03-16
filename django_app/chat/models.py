from django.db import models 
from users.models import CustomUser

class Chat(models.Model):
    """Tracking convo's btn users"""
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="chats_as_user1")
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="chats_as_user2")
    last_message = models.TextField(blank=True, null=True)
    last_message_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user1", "user2")
    
    def __str__(self):
        return f"Chat between {self.user1} and {self.user2}"
    
class Message(models.Model):
    """Storing private messages btn users"""
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Messages from {self.sender} in chat {self.chat.id}"
    
class Status(models.Model):
    """Users can post status updates visible to contacts"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="statuses")
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="status_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status by {self.user}"