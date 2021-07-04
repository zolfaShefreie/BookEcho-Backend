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
from . import filters
from utils.utils import CustomPageNumberPage
from utils.views import RelatedObjCreateView, UpdateWithPostMethodView, RelatedObjListView
from account.models import User
from account import permissions as account_permissions


class RequestCreateView(RelatedObjCreateView):
    related_obj_name = 'podcast_producer'
    queryset = User.objects.filter(user_type='p').exclude(info=None)
    permission_classes = (IsAuthenticated, permissions.ProducerNotReqUserPermission,
                          account_permissions.CompleteRegisterPermission)
    serializer_class = serializers.RequestSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RequestViewSet(ModelViewSet):
    queryset = models.Request.objects.all()
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = serializers.RequestSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticated(), permissions.ReqRetrievePermission(), ]

        return [IsAuthenticated(), permissions.ReqAccessDeleteUpdatePermission(), ]

    @transaction.atomic()
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class RequestAcceptByProducerView(UpdateWithPostMethodView):
    queryset = models.Request.objects.filter(status='p')
    permission_classes = (IsAuthenticated, permissions.ReqStatusChangeByProducerPermission,
                          account_permissions.CompleteRegisterPermission, )
    serializer_class = serializers.RequestAcceptByProducerSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class RequestRejectByProducerView(UpdateWithPostMethodView):
    queryset = models.Request.objects.filter(status='p')
    permission_classes = (IsAuthenticated, permissions.ReqStatusChangeByProducerPermission,
                          account_permissions.CompleteRegisterPermission, )
    serializer_class = serializers.RequestUpdateStatusSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def get_data(self):
        return {'status': 'r'}


class RequestDeadLineAcceptView(UpdateWithPostMethodView):
    queryset = models.Request.objects.filter(status='ac')
    permission_classes = (IsAuthenticated, permissions.ReqStatusChangeByApplicantPermission,)
    serializer_class = serializers.RequestUpdateStatusSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def get_data(self):
        return {'status': 'a'}


class RequestDeadLineRejectView(UpdateWithPostMethodView):
    queryset = models.Request.objects.filter(status='ac')
    permission_classes = (IsAuthenticated, permissions.ReqStatusChangeByApplicantPermission,)
    serializer_class = serializers.RequestUpdateStatusSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def get_data(self):
        return {'status': 'i'}


class ApplicantRequestList(RelatedObjListView):
    related_obj_name = 'applicant'
    permission_classes = (IsAuthenticated, )
    queryset = models.Request.objects.all()
    serializer_class = serializers.RequestSerializer
    paginator = CustomPageNumberPage()
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.RequestFilterSet

    def get_object(self):
        return self.request.user


class ProducerRequestList(RelatedObjListView):
    related_obj_name = 'podcast_producer'
    queryset = models.Request.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.RequestSerializer
    paginator = CustomPageNumberPage()
    filter_backends = (DjangoFilterBackend, account_permissions.CompleteRegisterPermission, )
    filter_class = filters.RequestFilterSet

    def get_object(self):
        return self.request.user
