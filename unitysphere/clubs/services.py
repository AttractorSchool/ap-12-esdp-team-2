from . import models
from . import exeptions


class ClubServices:
    """
    Предоставляет методы для управления действиями относящихся клубу.

    Attributes:
        club (Club): Клуб, в котором осуществляются операции.
    """

    def __init__(self, club):
        """
        Инициализирует объект ClubServices с указанным клубом.

        Args:
            club (Club): Клуб, для которого предоставляются услуги.
        """
        self.club = club

    def join(self, user):
        """
        Добавляет пользователя в члены клуба и обновляет количество участников.

        Args:
            user (User): Пользователь, который хочет вступить в клуб.

        Raises:
            clubs_exceptions.UserAlreadyInClubException: Если пользователь уже является членом клуба.
        """
        if self.club.members.filter(id=user.id).exists():
            raise exeptions.UserAlreadyInClubException
        self.club.members.add(user)
        self.club.members_count += 1
        self.club.save()

    def leave(self, user):
        """
        Удаляет пользователя из членов клуба и обновляет количество участников.

        Args:
            user (User): Пользователь, который хочет покинуть клуб.

        Raises:
            clubs_exceptions.UserNotInClubException: Если пользователь не является членом клуба.
        """
        if not self.club.members.filter(id=user.id).exists():
            raise exeptions.UserNotInClubException
        self.club.members.remove(user)
        self.club.members_count -= 1
        self.club.save()

    def like(self, user):
        """
        Добавляет пользователя в лайкнувшие клуб и обновляет количество лайков.

        Args:
            user (User): Пользователь, который хочет лайкнуть клуб.

        Raises:
            clubs_exceptions.UserLikeAlreadyExistsException: Если пользователь уже лайкнул клуб.
        """
        if self.club.likes.filter(id=user.id).exists():
            raise exeptions.UserLikeAlreadyExistsException
        self.club.likes.add(user)
        self.club.likes_count += 1
        self.club.save()

    def unlike(self, user):
        """
        Удаляет пользователя из лайкнувших клуб и обновляет количество лайков.

        Args:
            user (User): Пользователь, который хочет удалить свой лайк из клуба.

        Raises:
            clubs_exceptions.UserLikeDoesNotExistException: Если пользователь не лайкнул клуб.
        """
        if not self.club.likes.filter(id=user.id).exists():
            raise exeptions.UserLikeDoesNotExistException
        self.club.likes.remove(user)
        self.club.likes_count -= 1
        self.club.save()
