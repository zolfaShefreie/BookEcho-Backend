import enum


class Enum(enum.Enum):
    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]

    @classmethod
    def get_complete_choices(cls):
        return [(item.name, item.name) for item in cls]
