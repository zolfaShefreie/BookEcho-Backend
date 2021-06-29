from django.db import models

from utils.utils import Enum


class Choices:

    class RequestStatus(Enum):
        accepted = 'ac'
        rejected = 'r'
        pending = 'p'
        active = 'a'
        inactive = 'i'


class Request(models.Model):
    file = models.FileField(upload_to='pdf')
    applicant = models.ForeignKey('account.User', on_delete=models.CASCADE)
    podcast_producer = models.ForeignKey('account.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Choices.RequestStatus.choices(), default='p')
    deadline = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

