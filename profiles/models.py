from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _

class UserProfile(models.Model):
    SEX_CHOICES = (
        (True, _('Male')),
        (False, _('Female')),
        )

    user = models.ForeignKey(User, unique=True, editable=False)

    birthday = models.DateField(null=True, blank=True)
    sex = models.NullBooleanField(choices=SEX_CHOICES)

    is_public = models.BooleanField(default=True, db_index=True)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        if self.user.first_name == "" and self.user.last_name == "":
            return "%s's profile" % unicode(self.user)
        return self.get_name()

    def get_name(self):
        return " ".join([self.user.first_name, self.user.last_name])

    @permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), {'username': self.user.username})

    def can_show(self):
        return self.is_public

    def can_edit(self, user):
        return self.user == user

def user_created_handler(sender, instance, created, **kwargs):
    if created:
        instance.userprofile_set.create()

post_save.connect(user_created_handler,
                  sender=User,
                  dispatch_uid="users-profilecreation-signal")

from socialregistration import signals as social_signals
from socialregistration import models as social_models

def connect_facebook(user, profile, client, **kwargs):
    p = client.graph.get_object("me")
    if 'email' in p:
        user.email = p['email']
        user.save()

social_signals.connect.connect(
    connect_facebook,
    sender=social_models.FacebookProfile
)
