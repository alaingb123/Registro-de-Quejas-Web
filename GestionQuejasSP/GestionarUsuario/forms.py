from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_active', 'is_staff', 'is_admin']
        widgets = {
            'password': forms.PasswordInput(),  # Render password field as a password input
        }