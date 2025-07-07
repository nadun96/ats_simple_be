from django.db import models
from django.contrib.postgres.fields import ArrayField
from .application import Application


class Interview(models.Model):
    interview_id = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    scheduled_time = models.DateTimeField()
    calendar_event_id = models.CharField(max_length=200, blank=True, null=True)
    panel_user_ids = ArrayField(
        models.IntegerField(),
        size=10,
        blank=True,
        null=True,
        help_text="Array of user IDs for interview panel"
    )

    class Meta:
        db_table = 'interviews'
        ordering = ['scheduled_time']

    def __str__(self):
        return f"Interview for {self.application} - {self.scheduled_time.strftime('%Y-%m-%d %H:%M')}"
