from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver

class Timestamps(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False,
                                      db_index=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False,
                                      db_index=True)

    class Meta:
        abstract = True

class Paranoid(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True, default=None,
                                      editable=False, db_index=True)

    class Meta:
        abstract = True

    def delete(self, using=None):
        from datetime import datetime

        self.deleted_at = datetime.now()
        self.save()

@receiver(pre_save, sender=Paranoid, dispatch_uid="Paranoid_connector")
def paranoid(sender, **kwargs):
    from datetime import datetime
    sender.deleted_at = datetime.now()

class Ban(models.Model):
    approved_at = models.DateTimeField(null=True, blank=True,
                                       editable=False, db_index=True)
    banned_at = models.DateTimeField(null=True, blank=True,
                                     editable=False, db_index=True)

    class Meta:
        abstract = True
