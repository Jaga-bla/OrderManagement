from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password1', 'password2', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).exists()
        if user:
            raise ValidationError(('You can not use this email address.'))

        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']

class ProfileUpdateForm(forms.Form):
    image = forms.FileInput()