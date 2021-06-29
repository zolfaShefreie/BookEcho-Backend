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
    book_title = models.CharField(max_length=100),
    description = models.TextField(blank=True)
    pages = models.PositiveIntegerField()
    applicant = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='requests')
    podcast_producer = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='received_request')
    status = models.CharField(max_length=2, choices=Choices.RequestStatus.choices(), default='p')
    deadline = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

