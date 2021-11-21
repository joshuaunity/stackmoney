from django.forms import ModelForm
from django.contrib.auth.models import User, auth
from django import forms

# User/sign up form validation class 
class UserForm(ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']    