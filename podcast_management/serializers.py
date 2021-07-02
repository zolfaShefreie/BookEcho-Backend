from rest_framework import serializers

from . import models


class PodcastSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Podcast
        fields = "__all__"
        read_only_fields = ('id', 'delivery_date', 'req', 'is_private', 'is_active', 'score')

    def save(self, **kwargs):
        if not self.instance:
            self.validated_data['req'] = self.context.get('req')
        return super(PodcastSerializer, self).save(**kwargs)


class PodcastUpdateReadOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Podcast
        fields = "__all__"
        read_only_fields = ('id', 'req', )
