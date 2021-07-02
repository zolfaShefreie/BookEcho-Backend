from rest_framework.permissions import BasePermission


class IsProducerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'p'


class CompleteRegisterPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'p' and not hasattr(request.user, 'info')
