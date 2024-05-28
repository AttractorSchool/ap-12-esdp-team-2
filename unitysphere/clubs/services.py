from . import models
from . import exceptions


class ClubServices:
    """
    Предоставляет методы для управления действиями относящихся клубу.
    """
    @staticmethod
    def join(club, user):
        """
        Добавляет пользователя в члены клуба и обновляет количество участников.

        Args:
            club (Club): Клуб, в который хочет вступить пользователь.
            user (User): Пользователь, который хочет вступить в клуб.

        Raises:
            clubs_exceptions.UserAlreadyInClubException: Если пользователь уже является членом клуба.
        """
        if club.members.filter(id=user.id).exists():
            raise exceptions.UserAlreadyInClubException
        if club.is_private:
            if models.ClubJoinRequest.objects.filter(user=user, club=club).exists():
                raise exceptions.ClubJoinRequestAlreadyExistsException
            models.ClubJoinRequest.objects.create(club=club, user=user)
        else:
            club.members.add(user)
            club.members_count += 1
            club.save()

    @staticmethod
    def leave(club, user):
        """
        Удаляет пользователя из членов клуба и обновляет количество участников.

        Args:
            club (Club): Клуб, который хочет покинуть пользователь.
            user (User): Пользователь, который хочет покинуть клуб.

        Raises:
            clubs_exceptions.UserNotInClubException: Если пользователь не является членом клуба.
        """
        if not club.members.filter(id=user.id).exists():
            raise exceptions.UserNotInClubException
        club.members.remove(user)
        club.members_count -= 1
        club.save()

    @staticmethod
    def like(club, user):
        """
        Добавляет пользователя в лайкнувшие клуб и обновляет количество лайков.

        Args:
            club (Club): Клуб, который хочет лайкнуть пользователь.
            user (User): Пользователь, который хочет лайкнуть клуб.

        Raises:
            clubs_exceptions.UserLikeAlreadyExistsException: Если пользователь уже лайкнул клуб.
        """
        if club.likes.filter(id=user.id).exists():
            raise exceptions.UserLikeAlreadyExistsException
        club.likes.add(user)
        club.likes_count += 1
        club.save()

    @staticmethod
    def unlike(club, user):
        """
        Удаляет пользователя из лайкнувших клуб и обновляет количество лайков.

        Args:
            club (Club): Клуб, у которого хочет удалить свой лайк пользователь.
            user (User): Пользователь, который хочет удалить свой лайк из клуба.

        Raises:
            clubs_exceptions.UserLikeDoesNotExistException: Если пользователь не лайкнул клуб.
        """
        if not club.likes.filter(id=user.id).exists():
            raise exceptions.UserLikeDoesNotExistException
        club.likes.remove(user)
        club.likes_count -= 1
        club.save()


class ClubRequestServices:
    @staticmethod
    def approve(request: models.ClubJoinRequest):
        request.approved = True
        request.save()
        request.club.members.add(request.user)

    @staticmethod
    def reject(request: models.ClubJoinRequest):
        request.approved = False
        request.save()
        request.club.members.remove(request.user)


class FestivalServices:
    """
    Класс FestivalServices предоставляет статические методы для управления участием клубов в фестивалях.
    """

    @staticmethod
    def join(festival: models.Festival, club: models.Club):
        """
        Отправляет запрос на участие клуба в фестивале.

        Args:
            festival (models.Festival): Фестиваль, в который клуб хочет присоединиться.
            club (models.Club): Клуб, который хочет присоединиться к фестивалю.

        Raises:
            exceptions.ClubAlreadyExistsFestivalException: Если клуб уже участвует в фестивале.
            exceptions.FestivalRequestAlreadyExistsException: Если у клуба уже есть заявка на участие в фестивале.
        """
        if festival.approved_clubs.filter(id=club.id).exists():
            raise exceptions.ClubAlreadyExistsFestivalException
        if models.FestivalParticipationRequest.objects.filter(festival=festival, club=club).exists():
            raise exceptions.FestivalRequestAlreadyExistsException
        models.FestivalParticipationRequest.objects.create(club=club, festival=festival)

    @staticmethod
    def leave(festival: models.Festival, club: models.Club):
        """
        Удаляет клуб из фестиваля.

        Args:
            festival (models.Festival): Фестиваль, из которого клуб хочет выйти.
            club (models.Club): Клуб, который хочет выйти из фестиваля.

        Raises:
            exceptions.ClubNotExistsFestivalException: Если клуб не участвует в фестивале.
        """
        if not festival.approved_clubs.filter(id=club.id).exists():
            raise exceptions.ClubNotExistsFestivalException
        festival.approved_clubs.remove(club)


class FestivalRequestServices:

    @staticmethod
    def approve(request: models.FestivalParticipationRequest):
        """
        Одобряет запрос на участие клуба в фестивале.

        Args:
            request: Запрос на вступление фестиваль.
        """
        request.approved = True
        request.save()
        request.festival.approved_clubs.add(request.club)

    @staticmethod
    def reject(request: models.FestivalParticipationRequest):
        """
        Отклоняет запрос на участие клуба в фестивале.

        Args:
            request: Запрос на вступление фестиваль.
        """
        request.approved = False
        request.save()
