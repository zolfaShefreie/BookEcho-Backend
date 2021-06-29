from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_auth import views
from django.conf import settings
from django.utils.timezone import now
from rest_framework.generics import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from . import serializers
from . import models


class SignUpUserView(CreateAPIView):
    serializer_class = serializers.SignUpSerializer
    permission_classes = (AllowAny, )

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    http_method_names = ['get', 'patch', 'delete']
    queryset = models.User.objects.all()



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