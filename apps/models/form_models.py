from django.db import models
from general.mixins import SoftDeleteMixin, TimestampsMixin
from authentication.models import User


class Form(TimestampsMixin, SoftDeleteMixin):
    """ This are the forms that must be filled in the beggining of a Case or
     in the middle of an activity as the result of that activity """

    tag = models.CharField(
        'tag to recognize this form easier',
        max_length=10,
    )

    name = models.CharField(
        'name of the form',
        max_length=50,
    )

    description = models.CharField(
        'brief and concise description of the form',
        max_length=300,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='form_creator',
    )


class Question(TimestampsMixin, SoftDeleteMixin):
    """ will handle the questiong belonging to any form """

    form_concerned = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name='question_form',
    )

    label = models.CharField(
        'this is the queston indeed',
        max_length=50,
    )

    description = models.CharField(
        'Explanation of the question',
        max_length=300,
    )


class Option(TimestampsMixin, SoftDeleteMixin):
    """ """

    related_question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='related_question',
    )

    label = models.CharField(
        '',
        max_length=50,
    )

    option_type = models.CharField(
        'type of option...',
        max_length=30,
    )

    amount = models.BooleanField(
        '',
        default=False,
    )
    
    description = models.CharField(
        'brief and concise description of the option',
        max_length=300,
    )


class UserAnswer(TimestampsMixin, SoftDeleteMixin):
    """ Answer provided by a registered user """

    answered_question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answered_question'
    )

    answered_by = model.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answer_creator',
    )

    value = moedls.CharField(
        'answer gave by the user',
        max_length=100,
    )

    amount = models.IntegerField(
        '...',
        null=True,
    )
    
