from django.db import models
from django.contrib.auth.models import User
from .application import Application


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='tasks')
    assigned_to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    description = models.TextField()
    due_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'tasks'
        ordering = ['due_date', '-task_id']

    def __str__(self):
        return f"Task for {self.application} - {self.description[:50]}"
