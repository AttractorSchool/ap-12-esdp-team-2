from datetime import datetime

from django.db.models import Q
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework import mixins as drf_mixins
from rest_framework import permissions as drf_permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers, filtersets
from . import exceptions
from clubs import models
from . import permissions
from . import services
from . import mixins
from .models import ClubJoinRequest
from .serializers import ClubJoinRequestSerializer


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
    permission_classes = (permissions.ClubPermission,)
    ACTION_SERIALIZERS = {
        'club_action': serializers.ClubActionSerializer,
        'create': serializers.ClubCreateSerializer,
        'update': serializers.ClubUpdateSerializer,
        'retrieve': serializers.ClubDetailSerializer,
        'join_requests': serializers.ClubJoinRequestSerializer,
    }
    serializer_class = serializers.ClubListSerializer
    filterset_class = filtersets.ClubFilter

    @action(detail=True, methods=['post'], permission_classes=(IsAuthenticated,))
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
        action_name = serializer.validated_data['action']
        getattr(services.ClubServices, action_name)(club, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], permission_classes=(permissions.IsClubManager,))
    def join_requests(self, request, **kwargs):
        queryset = models.ClubJoinRequest.objects.filter(club=self.get_object())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    permission_classes = (permissions.ClubObjectsPermission,)
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
    permission_classes = (permissions.ClubObjectsPermission, )
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
    permission_classes = (permissions.ClubObjectsPermission, )
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
    permission_classes = (permissions.ClubObjectsPermission,)
    serializer_class = serializers.ClubGalleryPhotoSerializer


class FestivalViewSet(mixins.ClubActionSerializerMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления объектами Festival.

    Этот ViewSet предоставляет возможность выполнять стандартные операции CRUD (создание, чтение, обновление, удаление)
    для модели Festival, позволяя управлять фестивалями через RESTful API.

    Помимо стандартных операций CRUD, ViewSet предоставляет следующие действия:
    - festival_action: Выполнение действия (join, leave) с клубом на фестивале.

    Атрибуты:
        queryset: QuerySet всех фестивалей.
        ACTION_SERIALIZERS: Словарь с сериализаторами для различных действий.
        serializer_class: Сериализатор по умолчанию для создания или обновления фестиваля.
        permission_classes: Кортеж с классами разрешений, применяемых ко всем действиям.
    """
    queryset = models.Festival.objects.all()
    ACTION_SERIALIZERS = {
        'list': serializers.FestivalListSerializer,
        'retrieve': serializers.FestivalRetrieveSerializer,
        'festival_action': serializers.FestivalActionSerializer,
    }
    serializer_class = serializers.FestivalCreateOrUpdateSerializer
    permission_classes = (permissions.IsSuperUserOrReadOnly,)

    @action(detail=True, methods=['post'], permission_classes=[drf_permissions.IsAuthenticated])
    def festival_action(self, request, *args, **kwargs):
        """
        Выполняет действие join или leave с клубом на фестивале.

        Доступные действия:
        - join: Создает объект запроса FestivalParticipationRequest.
        - leave: Удалить клуб из фестиваля.

        Args:
            request: HTTP-запрос.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: HTTP-ответ с кодом состояния 204 (No Content) в случае успешного выполнения действия.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        festival = self.get_object()
        club = serializer.validated_data.get('club')
        if not club.managers.filter(id=request.user.id).exists():
            raise exceptions.NotClubManagerException
        action_name = serializer.validated_data.get('action')
        getattr(services.FestivalServices, action_name)(festival, club)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FestivalParticipationRequestViewSet(drf_mixins.ListModelMixin,
                                          drf_mixins.RetrieveModelMixin,
                                          viewsets.GenericViewSet):
    """
    ViewSet для управления объектами FestivalParticipationRequest.

    Этот ViewSet предоставляет возможность выполнять стандартные операции чтения (list, retrieve)
    для модели FestivalParticipationRequest, позволяя управлять запросами на участие в фестивалях через RESTful API.

    Помимо стандартных операций чтения, ViewSet предоставляет следующее действие:
    - request_action: Выполнение действия ('approve', 'reject') с запросом на участие в фестивале.

    Атрибуты:
        permission_classes: Кортеж с классами разрешений, применяемых ко всем действиям.
        queryset: QuerySet всех запросов на участие в фестивалях.
    """
    permission_classes = (permissions.IsSuperUserOrReadOnly,)
    queryset = models.FestivalParticipationRequest.objects.all()

    @action(detail=True, methods=['post'], permission_classes=[drf_permissions.IsAuthenticated])
    def request_action(self, request, *args, **kwargs):
        """
        Выполняет действие с запросом на участие в фестивале.

        Доступные действия:
        - approve: Одобрить запрос на участие в фестивале.
        - reject: Отклонить запрос на участие в фестивале.

        Args:
            request: HTTP-запрос.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: HTTP-ответ с кодом состояния 204 (No Content) в случае успешного выполнения действия.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action_name = serializer.validated_data.get('action')
        festival_request = self.get_object()
        getattr(services.FestivalRequestServices, action_name)(festival_request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора, используемого для текущего действия.

        Если действие request_action, используется FestivalRequestActionSerializer,
        иначе используется FestivalRequestSerializer.

        Returns:
            class: Класс сериализатора.
        """
        if self.action == 'request_action':
            return serializers.FestivalRequestActionSerializer
        return serializers.FestivalRequestSerializer


class ClubJoinRequestViewSet(drf_mixins.RetrieveModelMixin,
                             drf_mixins.ListModelMixin,
                             drf_mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    permission_classes = (permissions.ClubJoinRequestPermission,)
    queryset = ClubJoinRequest.objects.all()

    @action(detail=True, methods=['post'])
    def request_action(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request = self.get_object()
        action_name = serializer.validated_data.get('action')
        getattr(services.ClubRequestServices, action_name)(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action == 'request_action':
            return serializers.ClubJoinRequestActionSerializer
        return serializers.ClubJoinRequestSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Q(user=self.request.user) | Q(club__managers=self.request.user)).distinct()
