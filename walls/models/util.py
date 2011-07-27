from django.db import models

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

    def restore(self):
        self.deleted_at = None
        self.save()

    # Custom methods
    def is_deleted(self):
        return self.deleted_at is not None
    is_deleted.short_description = 'Deleted'
    is_deleted.boolean = True
    is_deleted.admin_order_field = 'deleted_at'

class Ban(models.Model):
    approved_at = models.DateTimeField(null=True, blank=True,
                                       editable=False, db_index=True)
    banned_at = models.DateTimeField(null=True, blank=True,
                                     editable=False, db_index=True)

    class Meta:
        abstract = True

    # Custom methods
    def is_approved(self):
        return self.approved_at is not None
    is_approved.short_description = 'Approved'
    is_approved.boolean = True
    is_approved.admin_order_field = 'approved_at'

    def is_banned(self):
        return self.banned_at is not None
    is_banned.short_description = 'Banned'
    is_banned.boolean = True
    is_banned.admin_order_field = 'banned_at'
