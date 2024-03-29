from rest_framework import serializers
from .models import Message, ScheduledMessage, MessageMedia

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageMedia
        fields = ['file']

class MessageSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, required=False)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'forwarded_from', 'media']

class ScheduledMessageSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, required=False)

    class Meta:
        model = ScheduledMessage
        fields = ['sender', 'receiver', 'content', 'scheduled_time', 'is_recurring', 'recurrence_frequency', 'recurrence_end_date', 'media']