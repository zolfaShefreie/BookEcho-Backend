from rest_framework import serializers

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
        read_only_fields = ('id', 'created_at', 'applicant', 'podcast_producer', 'status', )


class RequestUpdateStatusSerializer(serializers.ModelSerializer):
    status = ChoiceField(choices=models.Choices.RequestStatus.choices(), read_only=True)

    class Meta:
        model = models.Request
        fields = ('status', )

