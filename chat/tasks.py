from celery import shared_task
from .models import ScheduledMessage
from django.utils import timezone

@shared_task
def send_scheduled_messages():
    current_time = timezone.now()
    scheduled_messages = ScheduledMessage.objects.filter(scheduled_time__lte=current_time)

    for message in scheduled_messages:
        # Create a new message instance
        new_message = Message.objects.create(
            sender=message.sender,
            receiver=message.receiver,
            content=message.content
        )
        # If the scheduled message is recurring, update its scheduled time
        if message.is_recurring:
            update_recurring_message_schedule(message)
        else:
            # Delete the scheduled message if it's not recurring
            message.delete()

        # You can implement the sending logic here (e.g., sending an email or notification to the recipient)

def update_recurring_message_schedule(scheduled_message):
    # Update the scheduled time based on the recurrence frequency
    if scheduled_message.recurrence_frequency == 'daily':
        scheduled_message.scheduled_time += timezone.timedelta(days=1)
    elif scheduled_message.recurrence_frequency == 'weekly':
        scheduled_message.scheduled_time += timezone.timedelta(weeks=1)
    elif scheduled_message.recurrence_frequency == 'monthly':
        scheduled_message.scheduled_time += timezone.timedelta(days=30)  # Not precise, but a simple example

    # Check if the new scheduled time exceeds the recurrence end date
    if scheduled_message.recurrence_end_date and scheduled_message.scheduled_time > scheduled_message.recurrence_end_date:
        # Delete the scheduled message if it exceeds the recurrence end date
        scheduled_message.delete()
    else:
        # Save the updated scheduled message
        scheduled_message.save()