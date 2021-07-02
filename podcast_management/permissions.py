from rest_framework.permissions import BasePermission


class IsPodcastInactivePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return not obj.podcast.is_active


class IsPodcastActivePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.podcast.is_active
