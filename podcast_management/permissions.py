from rest_framework.permissions import BasePermission


class IsPodcastActivePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return not obj.podcast.is_active

