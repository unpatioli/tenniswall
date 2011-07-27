from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _

from util import Timestamps, Paranoid, Ban
from geo import Location

class DisplayManager(Location.objects.__class__):
    def __init__(self, only_approved=True):
        super(DisplayManager, self).__init__()
        self.only_approved = only_approved

    def get_query_set(self):
        query_set = super(DisplayManager, self).get_query_set().filter(
            deleted_at=None,
            banned_at=None
        )
        if self.only_approved:
            query_set = query_set.filter(approved_at__lte=datetime.now())
        return query_set

class PaidManager(DisplayManager):
    def get_query_set(self):
        return super(PaidManager, self).get_query_set().filter(price__gt = 0)

class FreeManager(DisplayManager):
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
    all_walls = DisplayManager(only_approved=False)
    objects = DisplayManager()
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
    is_paid.short_description = 'Paid'
    is_paid.boolean = True
    is_paid.admin_order_field = 'price'

    def can_edit(self, user):
        return self.reported_by == user

    def can_delete(self, user):
        return self.reported_by == user
