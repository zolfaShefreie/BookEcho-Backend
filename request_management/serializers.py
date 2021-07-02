from rest_framework import serializers
from django.utils.timezone import now, datetime

from . import models
from utils.utils import ChoiceField
from utils.validators import FileValidator


class RequestSerializer(serializers.ModelSerializer):
    status = ChoiceField(choices=models.Choices.RequestStatus.choices(), read_only=True)
    file = serializers.FileField(validators=[FileValidator(max_size=5242880, allowed_content_type=['application/pdf'])],
                                 required=True, allow_null=False)
    # podcast serializer

    class Meta:
        model = models.Request
        fields = "__all__"
        read_only_fields = ('id', 'created_at', 'applicant', 'podcast_producer', 'status', 'deadline', )

    def save(self, **kwargs):
        if not self.instance:
            request = self.context.get('request', None)
            self.validated_data['applicant'] = request.user
        return super().save(**kwargs)


class RequestUpdateStatusSerializer(serializers.ModelSerializer):
    status = ChoiceField(choices=models.Choices.RequestStatus.choices(), read_only=True)

    class Meta:
        model = models.Request
        fields = ('status', )


class RequestAcceptByProducerSerializer(serializers.ModelSerializer):
    deadline = serializers.DateField(required=True, allow_null=False)

    class Meta:
        model = models.Request
        fields = ('deadline', )

    def validate_deadline(self, value):
        if value <= datetime.date(now()):
            raise serializers.ValidationError("deadline must be after today")
        return value

    def save(self, **kwargs):
        self.instance.status = 'ac'
        return super().save(**kwargs)

