

class ClubActionSerializerMixin:
    ACTION_SERIALIZERS = {}

    def get_serializer_class(self):
        if serializer := self.ACTION_SERIALIZERS.get(self.action):
            return serializer
        return super().get_serializer_class()
