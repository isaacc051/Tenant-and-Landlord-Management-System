from django.db import models
from django.utils import timezone

class Message(models.Model):
    sender = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=100)
    content = models.TextField()
    read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    related_property = models.ForeignKey('properties.Property', on_delete=models.SET_NULL, 
                                         null=True, blank=True, related_name='messages')

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}: {self.subject}"

class Announcement(models.Model):
    landlord = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='announcements')
    properties = models.ManyToManyField('properties.Property', related_name='announcements')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False