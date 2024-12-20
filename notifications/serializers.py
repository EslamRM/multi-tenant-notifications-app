from rest_framework import serializers
from .models import Notifications


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = "__all__"


class NotificationSearchSerializer(serializers.Serializer):
    id = serializers.CharField()
    message = serializers.CharField()
    created_at = serializers.DateTimeField()
    read = serializers.BooleanField()
