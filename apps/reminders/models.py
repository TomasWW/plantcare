from django.db import models
from apps.core.models import TimeStampedModel

class Reminder(TimeStampedModel):
    class ReminderType(models.TextChoices):
        WATERING = 'watering', 'Watering'
        FERTILIZING = 'fertilizing', 'Fertilizing'
        PRUNING = 'pruning', 'Pruning'

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reminders')
    plant = models.ForeignKey('plants.Plant', on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=50,choices=ReminderType.choices, default=ReminderType.WATERING)  
    reminder_time = models.DateTimeField()
    repeat = models.PositiveIntegerField(null=True, blank=True, help_text='Repeat the task every X days')

    class Meta:
        db_table = 'reminders'

    def __str__(self):
        return f"{self.reminder_type} reminder for {self.plant} at {self.reminder_time}"

class ReminderHistory(TimeStampedModel):
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE, related_name='history')
    
    completed_date = models.DateField()
    class Meta:
        db_table = 'reminder_history'