from django.db import models
from general.mixins import SoftDeleteMixin, TimestampsMixin
from authentication.models import User, Role


class Service(TimestampsMixin, SoftDeleteMixin):
    """ Known Packages that will be used as type of packages """
    tag = models.CharField(
        'easy identifier of the service',
        max_length=10,
    )

    name = models.CharField(
        'Service Name',
        max_length=20,
    )

    description = models.CharField(
        'description of the Service',
        max_length=300,
    )


class Activity(TimestampsMixin, SoftDeleteMixin):
    """ Known Activities """
    title = models.CharField(
        'name of the activity'
        max_length=20,
    )

    description = models.CharField(
        'brief and concise description of the activity',
        max_length=300,
    )

    role_id = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='role_incharged',
        null=False,
    )

    service_id = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='parent_service'
    )


class ActivityOrder(TimestampsMixin, SoftDeleteMixin):
    """ Order that the activities must follow """
    previous_activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='previous_activity',
        null=True,
    )

    current_activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='current_activity',
        null=True,
    )


class FileOutput(TimestampsMixin, SoftDeleteMixin):
    """ file that must be provided by the user to finished the activity """

    activity_concerned = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='activity_concerned',
        null=False,
    )

    name = models.CharField(
        'name of the expected file',
        max_length=30,
    )

    description = models.CharField(
        'brief and concise description of what should be in the expected file',
        max_length=300,
    )

    file_extension = models.CharField(
        'extension that must have the expected file',
        max_length=6,
    )

    is_form = models.BooleanField(
        'indicates if the expected output of the activity is just a form',
        default=False,
    )

    related_form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name='expected_form',
        null=True,
    )


class FileInput(TimestampsMixin, SoftDeleteMixin):
    """ file which a user can see or download starting an activity,
     this is the resulted file of a previous activity"""

    activity_concerned = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='aimed_activity',
    )

    file_to_return = models.ForeignKey(
        FileOutPut,
        on_delete=models.CASCADE,
        related_name='file_returned'
    )
