

class ClubActionSerializerMixin:
    """
    Миксин, который позволяет использовать разные сериализаторы для разных действий в ViewSet-ах.

    Этот миксин позволяет определять разные сериализаторы для различных действий (например, 'create', 'update',
    'retrieve', и т. д.) внутри ViewSet-ов. Для этого необходимо создать атрибут класса ACTION_SERIALIZERS,
    который сопоставляет действия с соответствующими сериализаторами.

    Атрибуты:
        ACTION_SERIALIZERS (dict): Словарь, который сопоставляет действия с соответствующими сериализаторами.

    Пример использования:
        class MyViewSet(ClubActionSerializerMixin, viewsets.ModelViewSet):
            ACTION_SERIALIZERS = {
                'create': MyCreateSerializer,
                'update': MyUpdateSerializer,
                'retrieve': MyRetrieveSerializer,
            }
    """

    ACTION_SERIALIZERS = {}

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора для текущего действия.

        Если для текущего действия определен соответствующий сериализатор в атрибуте ACTION_SERIALIZERS,
        возвращается этот сериализатор. В противном случае используется сериализатор, определенный в родительском классе.

        Возвращает:
            Serializer: Класс сериализатора для текущего действия.
        """
        if serializer := self.ACTION_SERIALIZERS.get(self.action):
            return serializer
        return super().get_serializer_class()
