from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.db import transaction
from rest_auth import views
from django.conf import settings
from django.utils.timezone import now
from rest_framework.generics import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from . import serializers
from . import models
from utils.utils import CustomPageNumberPage
from utils.views import RelatedObjCreateView
from . import permissions


class SignUpUserView(CreateAPIView):
    serializer_class = serializers.SignUpSerializer
    permission_classes = (AllowAny, )

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserUpdateView(UpdateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user


class UserPrivateView(APIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)


class UserProfileView(RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.User.objects.filter(user_type='p')
    lookup_field = 'username'
    lookup_url_kwarg = 'username'


class ProducerList(ListAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = models.User.objects.filter(user_type='p')
    paginator = CustomPageNumberPage()


class AddChangeInfo(CreateAPIView):
    permission_classes = (IsAuthenticated, permissions.IsProducer, )
    serializer_class = serializers.InfoSerializer

    def post(self, request, *args, **kwargs):
        models.ProducerInfo.objects.filter(podcast_producer=request.user).delete()
        serializer = self.serializer_class(request.data, context={'user': request.user})
        return Response(serializer.data)



# class LoginUserView(APIView):
#     serializer_class = serializers.LoginUserSerializer
#     permission_classes = (AllowAny, )
#
#     def get_serializer_context(self):
#         return {
#             'request': self.request,
#             'format': self.format_kwarg,
#             'view': self
#         }
#
#     def get_serializer(self, *args, **kwargs):
#         serializer_class = self.serializer_class
#         kwargs['context'] = self.get_serializer_context()
#         return serializer_class(*args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data, status=status.HTTP_200_OK)