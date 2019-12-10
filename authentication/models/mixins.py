"""This module will handle the mixins that will be used in other models"""
from django.db import models


class SoftDeleteMixin(models.Model):
    """
    This mixin helps to know if an object was deleted. The delete operation will be in the soft delete way, that means, 
    that the entry WILL NOT be erased from the database but will be marked as thrased
    :trashed Boolean indicates if the objects was deleted
    :trashed_at Timestamp when the object was deleted
    """
    trashed = models.BooleanField('This field indicates if the objects was deleted.', default=False)
    trashed_at = models.DateTimeField("This field save the timestamp when the object was deleted.", default=None, null=True)

    class Meta:
        abstract = True


class TimestampsMixin(models.Model):
    """
    This mixin contains the elements that indicates when an entry was created
    :created_at contains the date when the entry was created
    :updated_at contains the date the entry was modified
    """
    created_at = models.DateTimeField("Cuando fue creada la entrada.", auto_now_add=True)
    updated_at = models.DateTimeField("Cuando fue actualizada la entrada por ultima vez.", auto_now=True)

    class Meta:
        abstract = True

