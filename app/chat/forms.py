from django.forms import ModelForm
from django import forms
from django.forms import Textarea
from .models import Message


class MessageSendForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {fields[0]: fields[0].title()}
        widgets = {fields[0]: Textarea(attrs={'class': 'form-control', 'placeholder': fields[0].title()})}