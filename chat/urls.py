from django.urls import path
from .views import SendMessageView, InboxView, ScheduledMessageView, ScheduledMessageListView

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send-message'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('schedule/', ScheduledMessageView.as_view(), name='schedule-message'),
    path('scheduled-messages/', ScheduledMessageListView.as_view(), name='scheduled-messages'),
]