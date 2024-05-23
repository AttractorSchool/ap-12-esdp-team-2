from rest_framework import status
from rest_framework.exceptions import APIException


class UserAlreadyInClubException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Пользователь уже состоит в группе'
    default_code = 'user_already_in_club'


class UserNotInClubException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Пользователь не состоит состоит в группе'
    default_code = 'user_not_in_club'


class ClubIsInactiveException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Данный клуб не активен'
    default_code = 'club_is_inactive'


class UserLikeAlreadyExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Лайк уже поставлен'
    default_code = 'user_like_already_exists'


class UserLikeDoesNotExistException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Нет лайка, которого можно было убрать'
    default_code = 'user_like_does_not_exist'


class InvalidClubActionExeption(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid club action'
    default_code = 'invalid_club_action'
