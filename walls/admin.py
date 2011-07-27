from datetime import datetime
from django.contrib import admin
from django import forms
from mapper.widgets import GoogleMapPickLocationWidget
from walls import models

class WallAdminForm(forms.ModelForm):
    is_approved = forms.BooleanField(required=False)
    is_banned = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(WallAdminForm, self).__init__(*args, **kwargs)
        self.fields['is_approved'] = forms.BooleanField(
            required=False,
            initial=self.instance.is_approved()
        )
        self.fields['is_banned'] = forms.BooleanField(
            required=False,
            initial=self.instance.is_banned()
        )

    class Meta:
        model = models.Wall

        widgets = {
            'location': GoogleMapPickLocationWidget(),
        }

    def clean_is_approved(self):
        is_approved = self.cleaned_data['is_approved']
        if is_approved:
            if not self.instance.approved_at:
                self.instance.approved_at = datetime.now()
        else:
            self.instance.approved_at = None

    def clean_is_banned(self):
        is_banned = self.cleaned_data['is_banned']
        if is_banned:
            if not self.instance.banned_at:
                self.instance.banned_at = datetime.now()
        else:
            self.instance.banned_at = None

    def clean(self):
        cleaned_data = super(WallAdminForm, self).clean()
        res = self._remove(['is_approved', 'is_banned'], cleaned_data)
        return res

    def _remove(self, fields, cleaned_data):
        cleaned_data = cleaned_data.copy()
        for field in fields:
            if field in cleaned_data:
                del cleaned_data[field]
        return cleaned_data

class WallAdmin(admin.ModelAdmin):
    form = WallAdminForm
    date_hierarchy = 'created_at'
    list_filter = ('approved_at',)
    list_display = ('__unicode__', 'is_paid', 'is_approved', 'is_banned',
                    'is_deleted')
    search_fields = ('address', 'description',)
    actions = ['make_approved', 'make_unapproved',
               'make_banned', 'make_unbanned',
               'mark_deleted', 'restore']

    class Media:
        js = (
            "https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js",
            "http://maps.google.com/maps/api/js?sensor=false",
        )

    ##################
    # Custom actions #
    ##################
    def _message(self, request, affected_rows_number, action_description):
        if affected_rows_number == 1:
            message_bit = "1 wall was"
        else:
            message_bit = "%s walls were" % affected_rows_number
        self.message_user(request,
            "%(message_bit)s %(action_description)s" % {
                'message_bit': message_bit,
                'action_description': action_description,
            }
        )

    def make_approved(self, request, queryset):
        qs = queryset.filter(approved_at=None)
        rows_updated = qs.update(approved_at=datetime.now())
        self._message(
            request,
            rows_updated,
            'successfully marked as approved.'
        )

    def make_unapproved(self, request, queryset):
        qs = queryset.exclude(approved_at=None)
        rows_updated = qs.update(approved_at=None)
        self._message(
            request,
            rows_updated,
            'successfully marked as unapproved.'
        )

    def make_banned(self, request, queryset):
        qs = queryset.filter(banned_at=None)
        rows_updated = qs.update(banned_at=datetime.now())
        self._message(
            request,
            rows_updated,
            'successfully banned.'
        )

    def make_unbanned(self, request, queryset):
        qs = queryset.exclude(banned_at=None)
        rows_updated = qs.update(banned_at=None)
        self._message(
            request,
            rows_updated,
            'successfully unbanned.'
        )

    def mark_deleted(self, request, queryset):
        qs = queryset.filter(deleted_at=None)
        walls_deleted = 0
        for wall in qs:
            wall.delete()
            walls_deleted += 1
        self._message(
            request,
            walls_deleted,
            'successfully marked deleted.'
        )
    
    def restore(self, request, queryset):
        qs = queryset.exclude(deleted_at=None)
        walls_restored = 0
        for wall in qs:
            wall.restore()
            walls_restored += 1
        self._message(
            request,
            walls_restored,
            'successfully restored.'
        )

admin.site.register(models.Wall, WallAdmin)
admin.site.register(models.WallComment)
