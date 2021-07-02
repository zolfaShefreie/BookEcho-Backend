from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db import transaction

from . import serializers
from . import models
from . import permissions
from utils.utils import CustomPageNumberPage
from utils.views import RelatedObjCreateView
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
        return super().post(self, request, *args, **kwargs)


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

