from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.forms import TextInput, Textarea
from .models import UserProfile, Book

attrs = {
    'class': 'from-control'
}


class UserProfileEdit(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'first_name', 'last_name', 'age', 'status', 'country', 'city', 'degree', 'organization']
        widgets = {
            'first_name': TextInput(attrs={'class': attrs['class'], 'placeholder': 'First name'}),
            'last_name': TextInput(attrs={'class': attrs['class'], 'placeholder': 'Last name'}),
            'status': TextInput(attrs={'class': attrs['class'], 'placeholder': 'Your status'}),
            'country': TextInput(attrs={'class': attrs['class'], 'placeholder': 'Country'}),
            'city': TextInput(attrs={'class': attrs['class'], 'placeholder': 'City'}),
            'organization': TextInput(attrs={'class': attrs['class'], 'placeholder': 'Organization'}),
            'degree': TextInput(attrs={'class': attrs['class'], 'placeholder': 'Your degree'})
        }


class CreateBookForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50, widget=TextInput(attrs={'class': attrs['class'], 'placeholder': 'Title'}))
    genre = forms.CharField(label='Genre', max_length=50, widget=TextInput(attrs={'class': attrs['class'], 'placeholder': 'Genre'}))
    subtitle = forms.CharField(label='Subtitle', max_length=100,widget=TextInput(attrs={'class': attrs['class'], 'placeholder': 'Subtitle'}))
    description = forms.CharField(label='Description', widget=Textarea(attrs={'class': attrs['class'], 'placeholder': 'Description'}))
    file = forms.FileField(label='File')
    cover = forms.ImageField(label='Cover', required=False)
