from rest_framework.permissions import BasePermission


class IsProducerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'p'


class CompleteRegisterPermission(BasePermission):
    def has_permission(self, request, view):
        return (request.user.user_type == 'p' and hasattr(request.user, 'info')) or request.user.user_type == 'n'
