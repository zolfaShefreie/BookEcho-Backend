from rest_framework import serializers


VALID_AUDIO = ["audio/mp3", 'audio/mpeg', 'audio/mp4', 'audio/basic', 'audio/x-midi', 'audio/webm', 'audio/vorbis',
               'audio/x-pn-realaudio', 'audio/vnd.rn-realaudio',
               'audio/x-pn-realaudio', 'audio/vnd.rn-realaudio', 'audio/wav', 'audio/x-wav','audio/ogg']


class FileValidator:

    code_size = 'file_max_size'
    code_content_type = 'invalid_extension'
    message = {'file_max_size': 'size of file is more than valid size',
               'invalid_extension': 'invalid format'}

    def __init__(self, max_size, allowed_content_type):
        self.max_size = max_size
        self.allowed_content_type = allowed_content_type

    def __call__(self, value):
        if value.size > self.max_size:
            raise serializers.ValidationError(code=self.code_size, detail=self.message[self.code_size])

        if value.content_type not in self.allowed_content_type:
            raise serializers.ValidationError(code=self.code_content_type, detail=self.message[self.code_content_type])