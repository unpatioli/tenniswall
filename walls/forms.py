from django import forms
from django.contrib.gis import forms as geoforms
from django.utils.translation import ugettext as _
from mapper.widgets import GoogleMapPickLocationWidget
from walls.models import Wall, WallComment, WallImage

class WallForm(geoforms.ModelForm):
    class Meta:
        model = Wall

        widgets = {
            'location': GoogleMapPickLocationWidget(),
        }

class WallCommentForm(forms.ModelForm):
    honeypot = forms.CharField(required=False,
                               label=_('If you enter anything in this field '\
                                       'your comment will be treated as spam'))

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value

    class Meta:
        model = WallComment

        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea({
                'class': 'span-23'
            })
        }

class WallImageForm(forms.ModelForm):
    class Meta:
        model = WallImage

        fields = ('image', 'title', 'description')
