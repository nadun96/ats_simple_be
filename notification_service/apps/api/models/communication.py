from django.db import models
from django.contrib.auth.models import User
from .application import Application


class Email(models.Model):
    email_id = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='emails')
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emails')
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=200)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'emails'
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.subject} - {self.recipient_email}"


class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notes'
        ordering = ['-created_at']

    def __str__(self):
        return f"Note by {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"
