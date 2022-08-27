from django.db import models
from django.urls import reverse
from uuid import uuid4
# Create your models here.
from main.models import UserProfile


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender_user')
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='recipient_user')
    has_unread = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'
        ordering = ['-user']
    
    def get_absolute_url(self):
        return reverse('chat', args=[str(self.pk)])
        
    def __str__(self):
        return f'{self.user} - {self.recipient}'
    
    
class Message(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4) 
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    recipient_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='recipient')
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-chat']
        
    def __str__(self):
        return f'{self.chat} {self.date}'
    
    
