from rest_framework.permissions import BasePermission


class ProducerNotReqUserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user != obj


class ReqAccessDeleteUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.applicant and obj.status == 'p'


class ReqRetrievePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in [obj.applicant, obj.podcast_producer]


