from django.contrib.auth.models import User
from .models import Status
from django import forms

from . import models
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    telephone = forms.CharField(max_length=10,help_text='Enter 10 digits only')
    gender = forms.CharField(max_length=1,help_text='Enter M or F')
    birthdate = forms.DateField(help_text='Required Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ['username','password','email','first_name','last_name','gender','telephone','birthdate']
        help_texts = {
            'username': None
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'id': 'post_txt', 
                'required': True, 
                'placeholder': 'How are you feeling...',
            })
        }
