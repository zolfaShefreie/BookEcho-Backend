from rest_framework import serializers
from django.utils.timezone import now, datetime

from . import models
from utils.validators import FileValidator, VALID_AUDIO


class PodcastSerializer(serializers.ModelSerializer):
    file = serializers.FileField(validators=[FileValidator(10485760, VALID_AUDIO +
                                                           ['application/zip', 'application/x-7z-compressed'])],
                                 allow_null=True)

    class Meta:
        model = models.Podcast
        fields = "__all__"
        read_only_fields = ('id', 'delivery_date', 'req', 'is_private', 'is_active', 'score')
    
    def to_internal_value(self, data):
        models.Podcast.objects.filter(req=self.context.get('req')).delete()
        return super().to_internal_value(data)

    def save(self, **kwargs):
        if not self.instance:
            self.validated_data['req'] = self.context.get('req')
        return super(PodcastSerializer, self).save(**kwargs)


class PodcastUpdateReadOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Podcast
        fields = "__all__"
        read_only_fields = ('id', 'req', 'delivery_date', 'score')

    def validate_is_active(self, value):
        if value and self.instance.file is None:
            raise serializers.ValidationError("podcast must has file")
        return value

    def save(self, **kwargs):
        if self.validated_data.get('is_active', None):
            self.validated_data['delivery_date'] = datetime.today()
        return super(PodcastUpdateReadOnlySerializer, self).save(**kwargs)


class PodcastScoreSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(max_value=10, min_value=0)

    class Meta:
        model = models.Podcast
        fields = ('score', )
