from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.contrib.auth.models import User as DjangoUser

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


