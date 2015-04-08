"""
Definition of forms.
"""

from django import forms
from app.models import SecureUser


"""
Custom user form to verfiy registration and login
"""
class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
      model = SecureUser
      fields = ('username', 'email', 'password')