from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(
        source='get_type_display',
        read_only=True
    )
    project_id = serializers.IntegerField(
        source='project.id',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Notification
        fields = [
            'id', 'type', 'type_display',
            'message', 'is_read', 'created_at',
            'project_id'
        ]
        read_only_fields = ['id', 'type', 'type_display', 'message', 'created_at']