from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from accounts.models import UserProfile

class NewUserForm(UserCreationForm):
    email = forms.EmailField(label=_('Email'))

    class Meta(UserCreationForm.Meta):
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError(
                _('User with the same email is already registered'))
        return email

class UserprofileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
