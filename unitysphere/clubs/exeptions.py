from rest_framework import status
from rest_framework.exceptions import APIException


class UserAlreadyInClubException(APIException):
    """
    Исключение, возникающее, когда пользователь пытается присоединиться к клубу, в котором он уже состоит.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Пользователь уже состоит в группе'
    default_code = 'user_already_in_club'


class UserNotInClubException(APIException):
    """
    Исключение, возникающее, когда пользователь не состоит в группе и пытается выполнить действие,
    требующее наличие его в клубе.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Пользователь не состоит в группе'
    default_code = 'user_not_in_club'


class ClubIsInactiveException(APIException):
    """
    Исключение, возникающее, когда происходит попытка выполнить действие с клубом, который не активен.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Данный клуб не активен'
    default_code = 'club_is_inactive'


class UserLikeAlreadyExistsException(APIException):
    """
    Исключение, возникающее, когда пользователь пытается поставить лайк, который уже был установлен.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Лайк уже поставлен'
    default_code = 'user_like_already_exists'


class UserLikeDoesNotExistException(APIException):
    """
    Исключение, возникающее, когда пользователь пытается удалить лайк, которого не существует.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Нет лайка, которого можно было убрать'
    default_code = 'user_like_does_not_exist'


class InvalidClubActionExeption(APIException):
    """
    Исключение, выбрасываемое при попытке выполнить недопустимое действие с клубом.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid club action'
    default_code = 'invalid_club_action'
