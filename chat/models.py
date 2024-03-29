from django.db import models
from user.models import CustomUser

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    forwarded_from = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

class MessageMedia(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='media/chatmedia/')
    timestamp = models.DateTimeField(auto_now_add=True)

class ScheduledMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='scheduled_messages')
    content = models.TextField()
    scheduled_time = models.DateTimeField()
    is_recurring = models.BooleanField(default=False)
    recurrence_frequency = models.CharField(max_length=20, blank=True, null=True)
    recurrence_end_date = models.DateField(blank=True, null=True)