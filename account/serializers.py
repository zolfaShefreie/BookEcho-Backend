from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.contrib.auth.models import User as DjangoUser
from rest_framework.fields import empty
from django.contrib.auth import authenticate, login

from . import models
from utils.utils import ChoiceField


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


class LoginUserSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    username_email = serializers.CharField(max_length=11, write_only=True, required=True)

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.user = None

    def validate(self, attrs):
        username_email = attrs.pop('username_email')
        if '@' in username_email:
            attrs['email'] = username_email
        else:
            attrs['username'] = username_email
        self.user = authenticate(self.context['request'], **attrs)
        return attrs

    def save(self, **kwargs):
        login(self.context['request'], self.user)

    # def to_representation(self, instance):
    #     ser = UserSerializer(instance=self.user)
    #     return ser.data


