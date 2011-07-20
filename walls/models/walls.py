from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _

from util import Timestamps, Paranoid, Ban
from geo import Location

class PaidManager(models.Manager):
    def get_query_set(self):
        return super(PaidManager, self).get_query_set().filter(price__gt = 0)

class FreeManager(models.Manager):
    def get_query_set(self):
        return super(FreeManager, self).get_query_set().filter(price = 0)

class Wall(Timestamps, Paranoid, Location, Ban):
    PERIOD_CHOICES = (
        (1, _('hour'),),
        (2, _('day'),),
        (3, _('month'),),
    )

    reported_by = models.ForeignKey(User, editable=False)

    address = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    price = models.IntegerField(default=0, db_index=True)
    period = models.PositiveIntegerField(choices=PERIOD_CHOICES,
                                         default=PERIOD_CHOICES[0][0])

    class Meta:
        app_label = 'walls'
        ordering = ['-created_at']

    # Managers
    objects = models.Manager()
    free = FreeManager()
    paid = PaidManager()

    # Utility methods
    def __unicode__(self):
        return self.address

    def get_absolute_url(self):
        return reverse('walls_detail', args=[self.pk,])

    # Custom methods
    def is_paid(self):
        return self.price > 0

    def can_edit(self, user):
        return self.reported_by == user

    def can_delete(self, user):
        return self.reported_by == user
