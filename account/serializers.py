from rest_framework import serializers
from rest_auth.utils import jwt_encode
import django.contrib.auth.password_validation as validators
from django.contrib.auth.models import User as DjangoUser
from rest_framework.fields import empty
from django.contrib.auth import authenticate, login
from rest_auth.models import TokenModel

from . import models
from utils.utils import ChoiceField
from utils.validators import FileValidator, VALID_AUDIO


class InfoSerializer(serializers.ModelSerializer):
    voice_sample = serializers.FileField(validators=[FileValidator(max_size=5242880, allowed_content_type=VALID_AUDIO)],
                                         required=True, allow_null=False)
    score = serializers.SerializerMethodField(method_name="get_score")

    class Meta:
        model = models.ProducerInfo
        fields = "__all__"
        extra_kwargs = {'podcast_producer': {'read_only': True}}
        
    def to_internal_value(self, data):
        models.ProducerInfo.objects.filter(podcast_producer=self.context.get('user', None)).delete()
        return super().to_internal_value(data)

    def save(self, **kwargs):
        self.validated_data['podcast_producer'] = self.context.get('user', None)
        instance = super().save(**kwargs)
        return instance

    def get_score(self, obj):
        return 100


class UserSerializer(serializers.ModelSerializer):
    user_type = ChoiceField(choices=models.Choices.UserType.choices(), read_only=True)
    info = InfoSerializer(read_only=True)
    avatar = serializers.ImageField(allow_null=True)

    class Meta:
        model = models.User
        fields = ('id', 'username', "first_name", "last_name", "email", "is_superuser",
                  "user_type", "date_joined", "info", "avatar")
        read_only_fields = ('id', 'date_joined', "producer_info", "user_type", )

    # def to_internal_value(self, data):
    #     print(self.context)
    #     return super().save(*)


class SignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    user_type = ChoiceField(choices=models.Choices.UserType.choices(), required=True)

    class Meta:
        model = models.User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'user_type')

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
        self.token = jwt_encode(user)
        return user

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data['password']
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        data = UserSerializer(instance).data
        data['token'] = self.token
        return data


class UserSummery(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('id', 'username', 'first_name', 'last_name')


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
