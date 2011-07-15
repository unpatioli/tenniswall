from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from accounts.models import UserProfile

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput())

    password_retype = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput())

    email = forms.EmailField(max_length=75)

    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    def clean_password_retype(self):
        password = self.cleaned_data['password']
        password_retype = self.cleaned_data['password_retype']
        if password_retype != password:
            raise forms.ValidationError(_('Passwords do not match'))
        return password_retype

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError(_('This username is already taken'))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError(
                _('User with the same email is already registered'))
        return email

class UserprofileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
