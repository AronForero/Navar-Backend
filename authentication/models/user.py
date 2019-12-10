from django.core.validators import RegexValidator
from django.db import models
from authentication.models.mixins import SoftDeleteMixin, TimestampsMixin
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """ This Class provide the functions to administrate the user objects """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        This method must return user.
        :argument email Valid Email
        :argument password Valid Password
        """

        # if email is None, throw error
        if not email:
            raise ValueError('El usuario debe tener un email valido.')

        # fixing email formatting (e.g. transferring to lowercase)
        email = self.normalize_email(email)

        # creating user model
        user = self.model(email=email, **extra_fields)

        # setting password for our new user
        user.set_password(password)

        # saving to database
        user.save(using=self._db)

        # returning user
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Wrapper method for creating normal user.
        This method must return user.
        """

        # method input validation
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        # returning user
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Wrapper method for creating admin user.
        This method must return user.
        """

        # method input validation
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # returning user
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, SoftDeleteMixin, TimestampsMixin):
    # don't use username
    username = None

    email = models.EmailField(
        'Email address of the user.',
        validators=[
            RegexValidator(
                regex=r"(^[a-zA-Z0-9_.+-]+@+[a-zA-Z]+\.[a-zA-Z]+$)",
            ),
        ],
        unique=True,
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()


class Role(models.Model):
    """ This will be placed the user roles """

    tag = models.CharField(
        'tag to recognize the role easily',
        max_length=10,
    )

    name = models.CharField(
        'Role Name',
        max_length=15,
    )

    description = models.CharField(
        'Description of the role (task to do)',
        max_length=300,
    )


class UserRole(SoftDeleteMixin, TimestampsMixin):
    """
    In this model will be saved all the relations between the users and roles, what means what role or roles
    has got a specific user
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='related_user',
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='role',
    )


class AdditionalUserInformation(TimestampsMixin, SoftDeleteMixin):
    """
    Additional data that belongs to the user
    """

    LIMB_CHOICES = (
        ('RIGHT_LEG', 'pierna_derecha'),
        ('LEFT_LEG', 'pierna_izquierda'),
        ('RIGHT_ARM', 'brazo_derecho'),
        ('LEFT_ARM', 'brazo_izquierdo'),
    )

    AMPUTATION_LEVEL_CHOICES = (
        ('Level_tal', 'bla bla'),
    )

    SOCKET_CHOICES = (
        ('TYPE_1', 'TYPE_1'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    birthday = models.DateField()

    city = models.CharField(
        'City where the user lives',
        max_length=15,
    )

    address = models.CharField(
        'addres of where the user lives',
        max_length=50,
    )

    phone_number = models.CharField(
        'Phone Number of the user',
        null=True,
        max_length=15,
    )

    weight = models.FloatField(
        'Just required for patients. Weight of the patient in Kg',
        null=True,
    )

    amputated_limb = models.CharField(
        'Limb affected',
        choices=LIMB_CHOICES,
        null=True,
        max_length=10,
    )

    profession = models.CharField(
        'Occupation of the patient',
        max_length=30,
        null=True,
    )

    amputation_level = models.CharField(
        'Choices',
        choices=AMPUTATION_LEVEL_CHOICES,
        null=True,
        max_length=10,
    )

    socket_type = models.CharField(
        'Choices',
        choices=SOCKET_CHOICES,
        null=True,
        max_length=10,
    )
