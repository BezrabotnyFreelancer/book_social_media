from django import forms
from django.forms import ModelForm
from django.forms import TextInput, Textarea
from .models import UserProfile, Book, Comment

attrs = {
    'class': 'from-control',
    'placeholder': ['First name', 'Last name']
}


class UserProfileEdit(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'first_name', 'last_name', 'age', 'status', 'country', 'city', 'degree', 'organization']
        widgets = {x: TextInput(attrs={'class': attrs['class'], 'placeholder': x.title()}) for x in fields
                   if x != 'avatar' and x != 'age'}
        widgets.update({
            'first_name': TextInput(attrs={'class': attrs['class'], 'placeholder': attrs['placeholder'][0]}),
            'last_name': TextInput(attrs={'class': attrs['class'], 'placeholder': attrs['placeholder'][1]})
        })

        labels = {x: x.title() for x in fields}
        labels.update({'first_name': attrs['placeholder'][0],
                       'last_name': attrs['placeholder'][1]})


class CreateBookForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50,
                            widget=TextInput(attrs={'class': attrs['class'], 'placeholder': 'Title'}))
    
    genre = forms.CharField(label='Genre', max_length=50,
                            widget=TextInput(attrs={'class': attrs['class'], 'placeholder': 'Genre'}))
    
    subtitle = forms.CharField(label='Subtitle', max_length=100,
                               widget=TextInput(attrs={'class': attrs['class'], 'placeholder': 'Subtitle'}))
    
    description = forms.CharField(label='Description',
                                  widget=Textarea(attrs={'class': attrs['class'], 'placeholder': 'Description'}))
    
    file = forms.FileField(label='File')
    cover = forms.ImageField(label='Cover', required=False)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {'comment': Textarea(attrs={'class': attrs['class'], 'placeholder': fields[0].title()})}
        labels = {'comment': 'Add comment'}
