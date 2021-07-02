from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.db.models.query import QuerySet

from .utils import CustomPageNumberPage


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


class RelatedObjListView(CreateAPIView):
    paginator = CustomPageNumberPage()
    related_obj_name = ''
    queryset_rel_obj = None
    queryset = None

    def get_object(self):
        queryset = self.queryset_rel_obj
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            obj = self.get_object()
            queryset = queryset.filter({self.related_obj_name: obj}).order_by("-created_at")
        return queryset


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
