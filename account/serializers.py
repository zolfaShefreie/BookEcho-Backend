from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.contrib.auth.models import User as DjangoUser
from rest_framework.fields import empty
from django.contrib.auth import authenticate, login
from rest_auth.models import TokenModel

from . import models
from utils.utils import ChoiceField


class InfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProducerInfo
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    user_type = ChoiceField(choices=models.Choices.UserType.choices(), read_only=True)
    producer_info = InfoSerializer(read_only=True, source='info')

    class Meta:
        model = models.User
        fields = ('id', 'username', "first_name", "last_name", "email", "is_superuser",
                  "user_type", "date_joined", "producer_info", "avatar")


class SignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    user_type = ChoiceField(choices=models.Choices.UserType.choices(), required=True)

    class Meta:
        model = models.User
        fields = ('id', 'user_name', 'first_name', 'last_name', 'email', 'password', 'user_type')

    def to_internal_value(self, data):
        models.User.objects.filter(user_type='p', info=None).delete()
        return super().to_internal_value(data)

    def validate_password(self, value):
        user = None
        if self.instance:
            user = DjangoUser(username=self.instance.mobile_number, first_name=self.instance.first_name,
                              last_name=self.instance.last_name, email=self.instance.email)
        else:
            try:
                user = DjangoUser(username=self.initial_data['email'],
                                  first_name=self.initial_data.get("first_name", None),
                                  last_name=self.initial_data.get("last_name", None))
            except KeyError:
                pass
        validators.validate_password(password=value, user=user)
        return value

    def save(self, **kwargs):
        user = super().save(**kwargs)
        login(self.context['request'], user)
        return user

    def to_representation(self, instance):
        data = UserSerializer(instance).data
        return data


# class LoginUserSerializer(serializers.Serializer):
#     password = serializers.CharField(write_only=True, required=True)
#     username_email = serializers.CharField(max_length=11, write_only=True, required=True)
#
#     def __init__(self, instance=None, data=empty, **kwargs):
#         super().__init__(instance, data, **kwargs)
#         self.user = None
#         self.token = None
#
#     def to_internal_value(self, data):
#         models.User.objects.filter(user_type='p', info=None).delete()
#         return super().to_internal_value(data)
#
#     def validate(self, attrs):
#         username_email = attrs.pop('username_email')
#         if '@' in username_email:
#             attrs['email'] = username_email
#         else:
#             attrs['username'] = username_email
#         self.user = authenticate(self.context['request'], **attrs)
#         return attrs
#
#     def save(self, **kwargs):
#         login(self.context['request'], self.user)
#         self.token = TokenModel.objects.create()
#
#
#     def to_representation(self, instance):
#         data = UserSerializer(self.user).data
#         return data
