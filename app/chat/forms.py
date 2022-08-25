from django import forms
from django.forms import Textarea, TextInput


class ChatForm(forms.Form):
    username = forms.CharField(label='Username', max_length=16, widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Input an username'
    }))
    
    
class MessageForm(forms.Form):
    body = forms.CharField(label='Message', widget=Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Write a message ...'
    }))
    
    files = forms.FileField(required=False)