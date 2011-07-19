from django import forms
from django.contrib.comments import CommentForm
from django.utils.translation import ugettext as _

class CustomCommentForm(CommentForm):

    name = forms.CharField(label=_("Name"), max_length=50, widget=forms.HiddenInput)
    email = forms.EmailField(label=_("Email address"), widget=forms.HiddenInput)
    url = forms.URLField(label=_("URL"), required=False, widget=forms.HiddenInput)
