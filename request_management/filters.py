from django_filters import FilterSet
import django_filters
import datetime
import pytz
from django.db.models import Q

from . import models
from utils.utils import ChoiceFilter


class RequestFilterSet(FilterSet):
    status = ChoiceFilter(enum_choices=models.Choices.RequestStatus)

    class Meta:
        model = models.Request
        fields = ['status', ]
