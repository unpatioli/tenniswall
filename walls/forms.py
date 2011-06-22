from django import forms

class AddWallForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    address = forms.CharField(max_length=500)
    lat = forms.FloatField()
    lon = forms.FloatField()

    def clean(self):
        """
        Changes form's cleaned_data to contain 'location' dict instead of
        lat and lon attributes
        """
        lat = self.cleaned_data.pop('lat')
        lon = self.cleaned_data.pop('lon')

        self.cleaned_data['location'] = {
            'lat': lat,
            'lon': lon,
        }
        return self.cleaned_data


