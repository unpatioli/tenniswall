from django.contrib.gis import forms as geoforms
from mapper.widgets import GoogleMapPickLocationWidget
from walls.models import Wall

class WallForm(geoforms.ModelForm):
    class Meta:
        model = Wall

        widgets = {
            'location': GoogleMapPickLocationWidget(),
        }
