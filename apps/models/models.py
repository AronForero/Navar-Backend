from django.db import models
from general.mixins import SoftDeleteMixin, TimestampsMixin
from authentication.models import User
from apps.models.abstract_models import Service
from apps.models.form_models import Form


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


class UserRequest(TimestampsMixin, SoftDeleteMixin):
    """ Relates the users and the requests to have a control of who can
     participate in a request/case """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='related_user_request',
    )

    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        related_name='related_request_user'
    )

    leader = models.BooleanField(
        'indicates if the user is the leader of the request or case',
        default=False,
    )


class RequestService(TimestampsMixin, SoftDeleteMixin):
    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        related_name='request_owner',
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='service_requested'
    )

    price = models.IntegerField(
        'Price of the service requested',
    )

    quantity = models.IntegerField(
        'amount of products requested from this service',
    )


class ActivityRequest(TimestampsMixin, SoftDeleteMixin):
    """ Activity that belongs to the choosen service in the request """

    ACTIVITY_STATE_CHOICES = (
        ('READY', 'Por Iniciar'),
        ('IN_PROGRESS', 'En Progreso'),
        ('FINISHED', 'Finalizada'),
    )

    title = models.CharField(
        'name of the activity, brougth from the activity model',
        max_length=20,
    )

    description = models.CharField(
        'brief and concise description of the activity, brougth from the activity model',
        max_length=300,
    )

    request_service = models.ForeignKey(
        RequestService,
        on_delete=models.CASCADE,
        related_name='request_service_concerned',
    )

    user_on_charge = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_on_charge',
    )

    activity_state = models.CharField(
        'State where the activity is',
        choices=ACTIVITY_STATE_CHOICES,
        max_length=15,
    )


class ActivityRequestComment(TimestampsMixin):
    """This model will store the comments in any activity in the case/request"""

    activity_request = models.ForeignKey(
        ActivityRequest,
        on_delete=models.CASCADE,
        related_name='activity_request_owner'
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

    parent_comment = models.ForeignKey(
        ActivityRequestComment,
        on_delete=models.CASCADE,
        related_name='parent_comment'
    )


class ActivityRequestPrevious(TimestampsMixin, SoftDeleteMixin):
    """ indicates the order of the activities in the case/request """
    activity_previous = models.ForeignKey(
        ActivityRequest,
        on_delete=models.CASCADE,
        related_name='previous_specific_activity',
    )

    current_activity = models.ForeignKey(
        ActivityRequest,
        on_delete=models.CASCADE,
        related_name='current_specific_activity',
    )


class RequestFileOutput(TimestampsMixin):
    """ output file of a specific activity in the case/request """

    name = models.CharField(
        'name of the expected file, brought from the file output model',
        max_length=30,
    )

    description = models.CharField(
        'brief and concise description of the expected file, brought from the file output model',
        max_length=300,
    )

    file_extension = models.CharField(
        'extension of the expected file, brought from the file output model',
        max_length=6,
    )

    activity_request = models.ForeignKey(
        ActivityRequest,
        on_delete=models.CASCADE,
        related_name='activity_request_file_output',
    )

    is_form = models.BooleanField(
        'indicates if the expected file is just a form, brought from the file output model',
        default=False,
    )

    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name='file_output_form',
    )


class RequestFileInput(TimestampsMixin):
    """ file which a user can see or download starting an activity,
     this is the resulted file of a previous activity"""

    request_file_to_return = models.ForeignKey(
        RequestFileOutput,
        on_delete=models.CASCADE,
        related_name='request_file_output_concerned',
    )

    activity_request = models.ForeignKey(
        ActivityRequest,
        on_delete=models.CASCADE,
        related_name='activity_request_file_input',
    )


class File(TimestampsMixin):
    """ This will handle the path in the dirs of each of the files uploaded to the platform """

    filename = models.CharField(
        'name of the file uploaded',
        max_length=30,
    )

    description = models.CharField(
        'brief and concise description of the uploaded file, should be kind of unique for each version of the same file',
        max_length=300,
    )

    path = models.CharField(
        'path of the dir where the file was stored',
        max_length=100,
    )

    output_file = models.ForeignKey(
        RequestFileOutput,
        on_delete=models.CASCADE,
        related_name='version_of_file',
    )


class Quotation(TimestampsMixin, SoftDeleteMixin):
    """ This class will handle the quotation data """

    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quotation_reviewer',
    )

    reviewed_at = models.DateTimeField(
        'When the quotation is reviewed',
        null=True,
    )

    authorized_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quotation_authorizer',
    )

    authorized_at = models.DateTimeField(
        'When the request is authorized',
        null=True,
    )

    area = models.CharField(
        'area?',
        max_length=10,
    )

    description = models.CharField(
        'brief and concise description of the current quotation',
        max_length=300,
    )

    economic_proposal = models.IntegerField(
        'amount of money that could cost the product',
    )

    terms = models.CharField(
        'terms??',
        max_length=100,
    )

    activity_parent = models.ForeignKey(
        ActivityRequest,
        on_delete=models.CASCADE,
        related_name='activity_request_parent',
        null=True,
    )

############################## CASE'S MODELS #####################################


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

    requirement_type = models.CharField(
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
        'Code of the Case (Automatically set)',
        max_length=15,
        unique=True,
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
