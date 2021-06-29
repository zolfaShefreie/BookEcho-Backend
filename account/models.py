from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from utils.utils import Enum


class Choices:

    class UserType(Enum):
        podcast_producer = 'p'
        normal = 'n'


class User(AbstractUser):
    email = models.EmailField(null=False)
    user_type = models.CharField(max_length=True, choices=Choices.UserType.choices(), null=False)
    avatar = models.ImageField(upload_to='avatar', null=True)
    USERNAME_FIELD = "email"


class ProducerInfo(models.Model):
    voice_sample = models.FileField(upload_to="voice_sample")
    score = models.PositiveIntegerField(default=0)
    podcast_producer = models.OneToOneField(User, on_delete=models.CASCADE)


