from rest_framework import serializers
from .models import LiveStream

class LiveStreamSerializer(serializers.ModelSerializer):
    """Live stream details"""
    host_name = serializers.CharField(source="host.username", read_only = True)

    class Meta:
        model = LiveStream
        fields = ["id", "host", "host_name", "title", "description", "is_active", "viewers_count", "start_time"]
        read_only_fields = ["id", "host", "is_active", "viewers_count", "start_time"]