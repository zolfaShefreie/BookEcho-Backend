from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status


class RelatedObjCreateView(CreateAPIView):
    related_obj_name = ''

    def create(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        context.update({self.related_obj_name: self.get_object()})
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UpdateWithPostMethodView(CreateAPIView):

    def get_data(self):
        return self.request.data

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=self.get_data(), partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()
