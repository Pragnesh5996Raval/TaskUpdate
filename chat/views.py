from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer, ScheduledMessageSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class SendMessageView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser, JSONParser]

    serializer_class = MessageSerializer

class InboxView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(receiver=user)

class ScheduledMessageView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser, JSONParser]

    serializer_class = ScheduledMessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class ScheduledMessageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = ScheduledMessageSerializer

    def get_queryset(self):
        user = self.request.user
        return ScheduledMessage.objects.filter(sender=user)