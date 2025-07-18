from django import forms

class AuthForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control',
        'required': True
    }))
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
        'required': True
    }))
