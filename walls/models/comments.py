from django.contrib.auth.models import User
from django.db import models
from util import Timestamps, Paranoid, Ban
from walls import Wall

class PublicManager(models.Manager):
    def get_query_set(self):
        return super(PublicManager, self).get_query_set().filter(is_public = True)

class PrivateManager(models.Manager):
    def get_query_set(self):
        return super(PrivateManager, self).get_query_set().filter(is_public = False)

class WallComment(Timestamps, Paranoid, Ban):
    author = models.ForeignKey(User, editable=False)
    wall = models.ForeignKey(Wall, editable=False)

    ip = models.IPAddressField(blank=True, null=True, editable=False)
    comment = models.TextField()

    is_public = models.BooleanField(default=True)

    class Meta:
        app_label = 'walls'
        ordering = ['created_at']

    # Managers
    objects = models.Manager()
    public = PublicManager()
    private = PrivateManager()

    # Utility methods
    def __unicode__(self):
        return self.comment

    def can_edit(self, user):
        return self.author == user

    def can_delete(self, user):
        return self.author == user
