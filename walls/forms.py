from django.contrib.gis import forms as geoforms
from mapper.widgets import GoogleMapPickLocationWidget
from walls.models import FreeWall, PaidWall

class LocationWidgets:
    widgets = {
        'location': GoogleMapPickLocationWidget()
    }

class FreeWallForm(geoforms.ModelForm):
    class Meta(LocationWidgets):
        model = FreeWall

class PaidWallForm(geoforms.ModelForm):
    class Meta(LocationWidgets):
        model = PaidWall
