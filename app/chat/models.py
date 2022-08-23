from django.db import models
from django.db.models import Max
from django.contrib.auth import get_user_model
# Create your models here.


class Message(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='from_user', null=True, blank=True)
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='to_user', null=True, blank=True)
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def send_message(from_user, to_user, body):
        sender_message = Message(
            user=from_user,
            sender=from_user,
            recipient=to_user,
            body=body,
            is_read=True
        )
        sender_message.save()
        
        recipient_message = Message(
            user=to_user,
            sender=from_user,
            recipient=from_user,
            body=body
        )
        recipient_message.save()
        
        return sender_message
    
    def get_messages(user):
        users = []
        messages = Message.objects.filter(user=user).values('recipient').annotate(last=Max('date')).order_by('-last')

        for message in messages:
            users.append({
                'user': get_user_model().objects.get(pk=message['recipient']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()
            })
            
        return users