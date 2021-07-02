from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db import transaction

from . import serializers
from . import models
from . import permissions
# from . import filters
from utils.utils import CustomPageNumberPage
from utils.views import RelatedObjCreateView, UpdateWithPostMethodView, RelatedObjListView
from account.models import User
from request_management.models import Request
from request_management.permissions import ReqStatusChangeByProducerPermission
from account import permissions as account_permissions


class PodcastCreateView(RelatedObjCreateView):
    related_obj_name = 'req'
    queryset = Request.objects.filter(status='a')
    serializer_class = serializers.PodcastSerializer
    permission_classes = (IsAuthenticated, ReqStatusChangeByProducerPermission, )
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class PodcastUpdateView(UpdateAPIView):
    queryset = Request.objects.filter(status='a').exclude(podcast=None)
    serializer_class = serializers.PodcastSerializer
    permission_classes = (IsAuthenticated, ReqStatusChangeByProducerPermission,
                          permissions.IsPodcastInactivePermission,)
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def get_object(self):
        obj = super().get_object()
        return obj.podcast


class PodcastActiveView(UpdateWithPostMethodView):
    queryset = Request.objects.filter(status='a').exclude(podcast=None)
    serializer_class = serializers.PodcastUpdateReadOnlySerializer
    permission_classes = (IsAuthenticated, ReqStatusChangeByProducerPermission,
                          permissions.IsPodcastInactivePermission,)
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def get_data(self):
        return {
            'is_active': True
        }

    def get_object(self):
        obj = super().get_object()
        return obj.podcast
