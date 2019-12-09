from django.db import models
from apps.models import mixins
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
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

    phone_number = models.CharField(
        'Phone Number of the user',
        null=True,
        max_length=15,
    )

    # picture = ProcessedImageField(
    #     upload_to=user_picture_path,
    #     processors=[ResizeToFit(512, 512)],
    #     format='JPEG',
    #     options={'quality': 60},
    #     null=True,
    #     blank=True
    # )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    # def save(self, *args, **kwargs):
    #     if self.picture.name is not None and self.picture.name != '' and self.picture.name.find("avatar_") == -1:
    #         extension = os.path.splitext(self.picture.name)[-1]
    #         self.picture.name = "{}_{}{}".format(
    #             'avatar',
    #             secrets.token_hex(3),
    #             extension,
    #         )
    #     super(User, self).save(*args, **kwargs)

