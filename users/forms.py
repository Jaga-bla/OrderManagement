from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.forms import ValidationError
from layout.models import Company

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label=('Email'),
        help_text=('Required. Enter an existing email address.'))
    CHOICES = (
        ('Yes','Yes'),
        ('No','No')
    )
    new_company = forms.ChoiceField(choices = CHOICES)
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

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class CompanyCreateForm(forms.ModelForm):
    name = forms.CharField(label="Enter your company name")
    password = forms.CharField(label="Enter your company password")
    class Meta:
        model = Company
        fields = ['name', 'password']

class CompanyLoginForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(label="Enter your company's key")
    class Meta:
        model = Company
        fields = ['name', 'password']