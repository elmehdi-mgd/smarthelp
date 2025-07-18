from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[('utilisateur', 'Utilisateur'), ('technicien', 'Technicien')], required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role') 