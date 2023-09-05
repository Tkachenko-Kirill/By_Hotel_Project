from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from PIL import Image

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserSelectForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(groups='1'))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'profile_image']