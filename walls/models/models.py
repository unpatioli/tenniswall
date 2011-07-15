from django.contrib.auth.models import User
from django.db import models

from walls.models.util import Timestamps, Paranoid, Ban
from walls.models.geo import Location

class Wall(Timestamps, Paranoid, Location, Ban):
    reported_by = models.ForeignKey(User, editable=False)
    address = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        app_label = 'walls'

class PaidWall(Wall):
    PERIOD_CHOICES = (
        (1, "day",),
        (2, "month",),
    )
    price = models.IntegerField()
    period = models.PositiveIntegerField(choices=PERIOD_CHOICES)

class FreeWall(Wall):
    pass
