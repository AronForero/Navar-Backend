from django.db import models
from apps.models.mixins import SoftDeleteMixin, TimestampsMixin


class Service(TimestampsMixin, SoftDeleteMixin):
    """
    Also Known as Packages
    """
    tag = models.CharField(
        'tag to recognize it easily',
        max_length=10,
    )

    name = models.CharField(
        'Name of the service',
        max_length=20,
    )

    description = models.CharField(
        'Short description of the service',
        max_length=300,
    )
