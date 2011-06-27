from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver

class Timestamps(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

@receiver(pre_save, sender=Timestamps, dispatch_uid="Timestamp_connector")
def paranoid(sender, **kwargs):
    import datetime
    sender.deleted_at = datetime.datetime.now()

class Location(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()

class Ban(models.Model):
    approved_at = models.DateTimeField(null=True, blank=True)
    banned_at = models.DateTimeField(null=True, blank=True)

# Create your models here.
class Wall(Timestamps, Location, Ban):
    reported_by = models.ForeignKey(User)
    address = models.CharField(max_length=250)

    class Meta:
        abstract = True

class PaidWall(Wall):
    PERIOD_CHOICES = (
        (1, "day",),
        (2, "month",),
    )
    price = models.IntegerField()
    period = models.PositiveIntegerField(choices=PERIOD_CHOICES)

class FreeWall(Wall):
    pass