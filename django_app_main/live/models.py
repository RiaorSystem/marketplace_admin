from django.db import models 
from users.models import CustomUser

class LiveStream(models.Model):
    """Tracks live stream sessions"""
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="hosted_streams")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    viewers_count = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.host.username}"