from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=45,
                               label='',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control mb-3',
                                   'placeholder': 'Nom d\'utilisateur'}))
    password = forms.CharField(max_length=30,
                               label='',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control mb-3',
                                   'placeholder': 'Mot de passe'}))
