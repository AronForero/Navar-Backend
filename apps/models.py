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


# class RequestState(models.Model):
#     """States that the Request can take"""
#     tag = models.CharField(
#         'easy identifier of the state',
#         max_length=10,
#     )

#     name = models.CharField(
#         'State Name',
#         max_length=20,
#     )

#     description = models.CharField(
#         'description of the state',
#         max_length=300,
#     )


class Request(TimestampsMixin, SoftDeleteMixin):

    STATE_CHOICES = (
        ('ESTADO_1', 'Estado 1'),
        ('ESTADO_2', 'Estado 2'),
    )

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

    state = models.CharField(
        'State of the request',
        choices=STATE_CHOICES,
        max_length=20,
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
        related_name='authorizer_user',
        null=True,
    )

    authorized_at = models.DateTimeField(
        'When the request is authorized',
        null=True,
    )

    inspected_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='inspector_user',
        null=True
    )

    inspected_at = models.DateTimeField(
        'When the request is accepted',
        null=True,
    )


class RequestComment(TimestampsMixin):
    """This model will store the comments in any request"""

    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        related_name='request_belongs'
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
        related_name='request_obj',
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


class Requirement(TimestampsMixin, SoftDeleteMixin):
    """
    This model will handle the data of the different types of requirements,
    that could be needed in a case
    """
    REQ_TYPE_CHOICES = (
        ('USE', 'USO'),
        ('FUNCTIONAL', 'FUNCIONAL'),
        ('OBJECT_RESISTANCE', 'RESISTENCIA_OBJETO'),
        ('TECNICAL_PRODUCTIVE', 'TECNICO_PRODUCTIVO'),
        ('NORMATIVE', 'NORMATIVO'),
    )

    type = models.CharField(
        'Type of requirement',
        choices=REQ_TYPE_CHOICES,
        max_length=20,
    )

    name = models.CharField(
        'Name of the requirement',
        max_length=50,
    )

    parameter = models.CharField(
        'Parameter of the requirement',
        max_length=50,
    )

    req_range = models.CharField(
        'Range ???',
        max_length=50,
    )

    measure = models.CharField(
        'Measure of the requirement',
        max_length=50,
    )

    importance = models.CharField(
        'Importance of the requirement',
        max_length=50,
    )

    approved = models.BooleanField(null=True)


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
        Request,
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


class CaseRequirement(TimestampsMixin, SoftDeleteMixin):
    """ Table that will handle the relation between the table of case and the table of requirement"""

    requirement = models.ForeignKey(
        Requirement,
        on_delete=models.CASCADE,
        related_name = 'requirement',
    )

    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='case_owner',
    )
