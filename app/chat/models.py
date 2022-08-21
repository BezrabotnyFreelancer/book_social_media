from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from uuid import uuid4
# Create your models here.
from main.models import UserProfile


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver')

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'

    def __str__(self):
        return f'{self.sender} {self.receiver}'

    def get_absolute_url(self):
        return reverse('chat_detail', args=[str(self.id)])


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender_user')
    receiver_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver_user')
    message = models.TextField()
    image = models.ImageField()
    file = models.FileField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f'{self.chat} {self.message}'
