import enum
from rest_framework import serializers


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