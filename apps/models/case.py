from django.db import models
from apps.models.mixins import SoftDeleteMixin, TimestampsMixin


class Case(TimestampsMixin, SoftDeleteMixin):
    """
    Here will be placed the basic information of the cases
    """
