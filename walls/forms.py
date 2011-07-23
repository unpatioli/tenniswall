from django import forms
from django.contrib.gis import forms as geoforms
from mapper.widgets import GoogleMapPickLocationWidget
from walls.models import Wall, WallComment

class WallForm(geoforms.ModelForm):
    class Meta:
        model = Wall

        widgets = {
            'location': GoogleMapPickLocationWidget(),
        }

class WallCommentForm(forms.ModelForm):
    class Meta:
        model = WallComment

        fields = ('comment',)
