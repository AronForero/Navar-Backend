from django.db import models
from general.mixins import SoftDeleteMixin, TimestampsMixin
from authentication.models import User


class Service(TimestampsMixin, SoftDeleteMixin):
    """ Also Known As Packages"""
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


class RequestState(models.Model):
    """States that the Request can take"""
    tag = models.CharField(
        'easy identifier of the state',
        max_length=10,
    )

    name = models.CharField(
        'State Name',
        max_length=20,
    )

    description = models.CharField(
        'description of the state',
        max_length=300,
    )


class Request(TimestampsMixin, SoftDeleteMixin):

    tag = models.CharField(
        'name of the case that the creator can set',
        max_length=15,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requester_user',
    )

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='related_patient',
    )

    state = models.ForeignKey(
        RequestState,
        on_delete=models.CASCADE,
        related_name='request_state',
    )

    estimated_delivery = models.DateTimeField(
        'Estimation of the end of the process',
    )

    conditions = models.CharField(
        'Extra Conditions that have to be in the product',
        max_length=300,
    )

    warranty = models.CharField(
        'Warranties that will have the product',
        max_length=300,
    )

    authorized_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authorizer',
    )

    authorized_at = models.DateTimeField(
        'When the request is authorized'
    )

    inspected_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='inspector',
    )

    inspected_at = models.DateTimeField(
        'When the request is accepted'
    )


class RequestComment(TimestampsMixin):
    """This model will store the comments in any request"""

    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        related_name='request_obj'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='creator_user',
    )

    content = models.CharField(
        'content of the comment',
        max_length=500,
    )


class RequestService(TimestampsMixin, SoftDeleteMixin):
    """ Services that will be related with a specific request """
    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        related_name='initial_request',
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='related_service',
    )

    price = models.FloatField(
        'Price of the service',
    )

    quantity = models.IntegerField(
        'Amount of products to create'
    )


class Case(TimestampsMixin, SoftDeleteMixin):
    """ Case the principal Object in the Db """
    code = models.CharField(
        'easy tag to recognize the obj',
        max_length=10,
    )

    tag = models.CharField(
        'Tag that the user will set',
        max_length=20,
    )

    request = models.ForeignKey(
        'Request that opens the case',
        on_delete=models.CASCADE,
        related_name='related_request',
    )

    end_date = models.DateTimeField(
        'Estimation of the date when the product will be delivered',
    )

    description = models.CharField(
        'Extra description of the case',
        max_length=300,
    )
