from django import forms
from django.forms.models import ModelForm
from django.forms import Textarea, TextInput
from .models import Message

attrs_parms = {'class': 'form-control'}

class ChatForm(forms.Form):
    username = forms.CharField(label='Username', max_length=16, widget=TextInput(attrs={
        'class': attrs_parms['class'],
        'placeholder': 'Input an username'
    }))
    
    
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        labels = {'body': 'Message'}
        widgets = {'body': Textarea(attrs={'class': attrs_parms['class'], 'placeholder': 'Enter a message ...'})}
   