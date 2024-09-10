from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect
from django.views import generic
from .forms import RegisterUserForm, UserLoginForm, UserUpdateForm
from .models import User


class RegisterUserView(generic.FormView):
    """
    View для регистрации нового пользователя.

    Этот класс обрабатывает форму регистрации нового пользователя. Если пользователь уже аутентифицирован,
    его перенаправляют на главную страницу. Если форма успешно валидируется, новый пользователь создается и
    аутентифицируется, после чего происходит перенаправление на страницу, с которой пришел пользователь.
    """

    form_class = RegisterUserForm
    template_name = 'accounts/register_user.html'

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительный контекст в шаблон.

        Параметры:
            **kwargs: Дополнительные аргументы для контекста.

        Возвращает:
            dict: Контекст для рендеринга шаблона.
        """
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Центр сообществ - Регистрация'
        return ctx

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос для регистрации пользователя.

        Перенаправляет аутентифицированных пользователей на главную страницу. Если пользователь не аутентифицирован,
        вызывает родительский метод для рендеринга страницы регистрации.

        Параметры:
            request (HttpRequest): Объект запроса.

        Возвращает:
            HttpResponseRedirect или HttpResponse: Результат обработки запроса.
        """
        if self.request.user.is_authenticated:
            return redirect('index')
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Обрабатывает валидную форму регистрации.

        Если форма валидна, сохраняет нового пользователя, аутентифицирует его и перенаправляет на страницу
        успешного завершения регистрации.

        Параметры:
            form (RegisterUserForm): Валидная форма регистрации.

        Возвращает:
            HttpResponseRedirect: Перенаправление на URL, указанный в get_success_url.
        """
        if form.is_valid():
            user = form.save()
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        """
        Определяет URL для перенаправления после успешной регистрации.

        Возвращает URL, с которого пришел пользователь (HTTP_REFERER), или корневой URL ('/').

        Возвращает:
            str: URL для перенаправления.
        """
        success_url = self.request.META.get('HTTP_REFERER', '/')
        return success_url


class LoginUserView(LoginView):
    """
    View для страницы входа пользователя.

    Этот класс обрабатывает страницу входа в систему, используя форму для входа пользователя.

    Атрибуты:
        form_class (forms.Form): Форма для входа пользователя.
        template_name (str): Путь к шаблону страницы входа.
    """

    form_class = UserLoginForm
    template_name = 'accounts/login_user.html'


class UserDetailView(generic.DetailView):
    """
    View для отображения деталей пользователя.

    Этот класс обрабатывает отображение страницы с деталями пользователя. Если профиль пользователя
    скрыт, вызывается исключение PermissionDenied. В противном случае, отображается страница с деталями пользователя.

    Атрибуты:
        model (models.Model): Модель пользователя для отображения.
        context_object_name (str): Имя объекта контекста для шаблона.
        template_name (str): Путь к шаблону страницы с деталями пользователя.
    """

    model = User
    context_object_name = 'user'
    template_name = 'accounts/user_detail.html'

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительный контекст в шаблон.

        Параметры:
            **kwargs: Дополнительные аргументы для контекста.

        Возвращает:
            dict: Контекст для рендеринга шаблона, включая название страницы.
        """
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = self.get_object()
        return ctx

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос для отображения деталей пользователя.

        Если профиль пользователя закрыт для отображения, возбуждается исключение PermissionDenied.
        В противном случае, вызывается родительский метод для рендеринга страницы.

        Параметры:
            request (HttpRequest): Объект запроса.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            HttpResponse: Результат обработки запроса.

        Исключения:
            PermissionDenied: Если профиль пользователя закрыт для отображения.
        """
        if not self.get_object().is_displayed_in_allies:
            raise PermissionDenied("Профиль пользователя закрыт")
        else:
            return super().get(request, *args, **kwargs)


class UserListView(generic.ListView):
    """
    View для отображения списка пользователей.

    Этот класс обрабатывает отображение списка пользователей с возможностью поиска и пагинации. Пользователи,
    которые не должны отображаться (определяется полем is_displayed_in_allies), исключаются из результатов.
    Также исключается текущий аутентифицированный пользователь из списка.

    Атрибуты:
        model (models.Model): Модель пользователя для отображения.
        context_object_name (str): Имя объекта контекста для шаблона.
        template_name (str): Путь к шаблону страницы со списком пользователей.
        paginate_by (int): Количество пользователей на одной странице.
        ordering (list): Список полей для сортировки пользователей.
    """

    model = User
    context_object_name = 'users'
    template_name = 'accounts/user_list.html'
    paginate_by = 10
    ordering = ['first_name', 'last_name']

    def get_queryset(self):
        """
        Возвращает отфильтрованный и отсортированный queryset пользователей.

        Фильтрация осуществляется по полю is_displayed_in_allies и по параметрам поиска из GET-запроса.
        Параметры поиска включают поиск по всем полям, интересам или имени. Также исключается текущий аутентифицированный пользователь.

        Параметры:
            None

        Возвращает:
            QuerySet: Отфильтрованный и отсортированный список пользователей.
        """
        qs = super().get_queryset().filter(is_displayed_in_allies=True)
        search_query = self.request.GET.get('search')
        search_field = self.request.GET.get('search-field')

        if search_query:
            if search_field == 'all':
                qs = User.objects.filter(
                    Q(profile__about__icontains=search_query) |
                    Q(profile__goals_for_life__icontains=search_query) |
                    Q(profile__interests__icontains=search_query) |
                    Q(first_name__icontains=search_query) |
                    Q(last_name__icontains=search_query)
                )
            elif search_field == 'interests':
                qs = User.objects.filter(
                    Q(profile__about__icontains=search_query) |
                    Q(profile__goals_for_life__icontains=search_query) |
                    Q(profile__interests__icontains=search_query)
                )
            elif search_field == 'name':
                qs = User.objects.filter(
                    Q(first_name__icontains=search_query) |
                    Q(last_name__icontains=search_query)
                )
            return qs.exclude(id=self.request.user.id)

        return User.objects.filter(is_displayed_in_allies=True).exclude(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search')
        context['search_field'] = self.request.GET.get('search-field')
        return context


class UserUpdateView(LoginRequiredMixin, generic.FormView):
    """
    View для обновления профиля пользователя.

    Этот класс обрабатывает страницу для обновления профиля текущего аутентифицированного пользователя.
    При GET-запросе отображает форму с текущими данными пользователя. При POST-запросе обновляет данные пользователя
    и перенаправляет его на страницу с обновленным профилем.

    Атрибуты:
        form_class (forms.Form): Форма для обновления профиля пользователя.
        template_name (str): Путь к шаблону страницы обновления профиля.
    """

    form_class = UserUpdateForm
    template_name = 'accounts/update_profile.html'

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос для отображения формы обновления профиля.

        Создает форму с текущими данными пользователя и добавляет её в контекст шаблона. Устанавливает заголовок страницы.

        Параметры:
            request (HttpRequest): Объект запроса.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            HttpResponse: Ответ с рендерингом шаблона формы обновления профиля.
        """
        form = self.form_class(instance=request.user)
        page_title = 'Изменить профиль'
        ctx = {
            'page_title': page_title,
            'form': form,
        }
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос для обновления данных профиля пользователя.

        При успешной валидации формы обновляет данные пользователя и перенаправляет его на страницу профиля.
        Если форма невалидна, возвращает ту же страницу с ошибками формы.

        Параметры:
            request (HttpRequest): Объект запроса.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            HttpResponse: Перенаправление на страницу профиля при успешной валидации формы, или рендеринг той же страницы с ошибками формы.
        """
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect(user.get_absolute_url())
        else:
            return self.render_to_response({'form': form})
