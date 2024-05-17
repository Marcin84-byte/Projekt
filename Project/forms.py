from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class ContactForm(forms.Form):
    name = forms.CharField(label='Name')
    surname = forms.CharField(label='Surname')
    email = forms.EmailField(label='Email')
    content = forms.CharField(label='Content', widget=forms.Textarea)


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Username', min_length=5, max_length=150)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password')
    password2 = forms.CharField(label='Confirm password')


class LoginViewForm(AuthenticationForm):
    username = forms.CharField(label='Username', min_length=5, max_length=150)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password')
