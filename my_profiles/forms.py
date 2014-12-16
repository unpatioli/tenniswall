from django import forms
from profiles.models import UserProfile
from profiles.widgets import CalendarWidget

class UserprofileForm(forms.ModelForm):
    class Meta:
        model = UserProfile

        widgets = {
            'birthday': CalendarWidget
        }
