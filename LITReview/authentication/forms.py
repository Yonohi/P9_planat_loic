from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=45, label='Nom d’utilisateur')
    password = forms.CharField(max_length=30, widget=forms.PasswordInput, label='Mot de passe')
