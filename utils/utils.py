import enum

import django_filters
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination


class Enum(enum.Enum):
    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]

    @classmethod
    def get_complete_choices(cls):
        return [(item.name, item.name) for item in cls]


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class ChoiceFilter(django_filters.ChoiceFilter):

    def __init__(self, *args, **kwargs):
        self.enum_choices = kwargs.pop("enum_choices", Enum({}))
        choices = self.enum_choices.get_complete_choices()
        kwargs["choices"] = choices
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        try:
            value = self.enum_choices[value].value
            return super(ChoiceFilter, self).filter(qs, value)
        except:
            return qs



class CustomPageNumberPage(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 1000
    page_size = 20