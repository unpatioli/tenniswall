from django import forms
from accounts.models import UserProfile

class UserprofileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
