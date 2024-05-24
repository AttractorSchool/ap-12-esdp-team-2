from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from . import serializers
from clubs import models
from .permissions import ClubPermission, ClubObjectsPermission
from . import services
from . import mixins


class ClubViewSet(mixins.ClubActionSerializerMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления клубами.

    Данный ViewSet предоставляет стандартные действия CRUD для модели Club,
    а также пользовательское действие `club_action`.

    Атрибуты:
        queryset (QuerySet): Базовый набор данных для этого ViewSet-а, включающий только активные клубы.
        permission_classes (tuple): Классы разрешений, применяемые к этому ViewSet-у.
        ACTION_SERIALIZERS (dict): Словарь, который сопоставляет действия с соответствующими сериализаторами.
        serializer_class (Serializer): Сериализатор, используемый по умолчанию для действий, не указанных в ACTION_SERIALIZERS.
    """
    queryset = models.Club.objects.filter(is_active=True)
    permission_classes = (ClubPermission,)
    ACTION_SERIALIZERS = {
        'club_action': serializers.ClubActionSerializer,
        'create': serializers.ClubCreateSerializer,
        'update': serializers.ClubUpdateSerializer,
        'retrieve': serializers.ClubDetailSerializer,
    }
    serializer_class = serializers.ClubListSerializer

    @action(detail=True, methods=['post'])
    def club_action(self, request, **kwargs):
        """
        Пользовательское действие для выполнения определенных операций с клубом.

        Параметры:
            request (Request): Объект запроса с данными.
            **kwargs: Дополнительные аргументы.

        Возвращает:
            Response: HTTP-ответ с статусом 204 (No Content) при успешном выполнении действия.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        club = self.get_object()
        club_services = services.ClubServices(club)
        action_name = serializer.validated_data['action']
        getattr(club_services, action_name)(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        """
        Возвращает набор данных для данного ViewSet-а.

        В зависимости от действия, возвращает оптимизированный queryset с использованием
        select_related и prefetch_related для уменьшения количества запросов к базе данных.

        Возвращает:
            QuerySet: Набор данных для текущего действия.
        """
        queryset = super().get_queryset()
        if self.action == 'retrieve':
            return (
                queryset
                .select_related('category', 'city', 'creater')
                .prefetch_related('members', 'partners', 'likes', 'managers')
            )
        elif self.action == 'list':
            return queryset.select_related('category')
        return queryset


class ClubServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления услугами клубов.

    Данный ViewSet позволяет выполнять стандартные операции CRUD (создание, чтение, обновление, удаление)
    для модели ClubService, предоставляя RESTful API для управления услугами клубов.

    Атрибуты:
        queryset (QuerySet): Базовый набор данных для этого ViewSet-а, включающий все услуги клубов.
        permission_classes (tuple): Классы разрешений, применяемые для проверки прав доступа к операциям с услугами клубов.
        serializer_class (Serializer): Сериализатор для преобразования данных модели ClubService в JSON.
    """
    queryset = models.ClubService.objects.all()
    permission_classes = (ClubObjectsPermission,)
    serializer_class = serializers.ClubServiceSerializer


class ClubEventViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления событиями клубов.

    Этот ViewSet предоставляет возможность управлять событиями клубов, включая создание, чтение, обновление и удаление.

    Атрибуты:
        queryset (QuerySet): Базовый набор данных для этого ViewSet-а, включающий все будущие события клубов.
        permission_classes (tuple): Классы разрешений, применяемые для проверки прав доступа к операциям с событиями клубов.
        serializer_class (Serializer): Сериализатор для преобразования данных модели ClubEvent в JSON.
    """
    queryset = models.ClubEvent.objects.filter(start_datetime__gte=datetime.now())
    permission_classes = (ClubObjectsPermission, )
    serializer_class = serializers.ClubEventSerializer


class ClubAdsViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления рекламными объявлениями клубов.

    Данный ViewSet позволяет выполнять стандартные операции CRUD (создание, чтение, обновление, удаление)
    для модели ClubAds, предоставляя RESTful API для управления рекламными объявлениями клубов.

    Атрибуты:
        queryset (QuerySet): Базовый набор данных для этого ViewSet-а, включающий все рекламные объявления клубов.
        permission_classes (tuple): Классы разрешений, применяемые для проверки прав доступа к операциям с рекламными объявлениями клубов.
        serializer_class (Serializer): Сериализатор для преобразования данных модели ClubAds в JSON.
    """
    queryset = models.ClubAds.objects.all()
    permission_classes = (ClubObjectsPermission, )
    serializer_class = serializers.ClubAdsSerializer


class ClubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра категорий клубов.

    Этот ViewSet предоставляет только чтение (GET) данных о категориях клубов.

    Атрибуты:
        queryset (QuerySet): Базовый набор данных для этого ViewSet-а, включающий только активные категории клубов.
        serializer_class (Serializer): Сериализатор для преобразования данных модели ClubCategory в JSON.
    """
    queryset = models.ClubCategory.objects.filter(is_active=True)
    serializer_class = serializers.ClubCategorySerializer


class ClubCityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра городов.

    Этот ViewSet предоставляет только чтение (GET) данных о городах.

    Атрибуты:
        queryset (QuerySet): Базовый набор данных для этого ViewSet-а, включающий все города.
        serializer_class (Serializer): Сериализатор для преобразования данных модели City в JSON.
    """
    queryset = models.City.objects.all()
    serializer_class = serializers.ClubCitySerializer


class ClubGalleryPhotoViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления фотографиями галереи клубов.

    Этот ViewSet предоставляет возможность выполнять стандартные операции CRUD (создание, чтение, обновление, удаление)
    для модели ClubGalleryPhoto, позволяя управлять фотографиями галереи клубов через RESTful API.

    Атрибуты:
        queryset (QuerySet): Базовый набор данных для этого ViewSet-а, включающий все фотографии галереи клубов.
        permission_classes (tuple): Классы разрешений, применяемые для проверки прав доступа к операциям с фотографиями галереи клубов.
        serializer_class (Serializer): Сериализатор для преобразования данных модели ClubGalleryPhoto в JSON.
    """
    queryset = models.ClubGalleryPhoto.objects.all()
    permission_classes = (ClubObjectsPermission,)
    serializer_class = serializers.ClubGalleryPhotoSerializer
