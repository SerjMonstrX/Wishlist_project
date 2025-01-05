from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from functools import wraps

from wishlist.models import Wishlist


class LoginANdAuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Класс, объединяющий общие настройки для проверки авторства пользователя"""

    def test_func(self):
        """Функция для проверки является ли пользователь автором рассылки"""
        mailing = self.get_object()
        return self.request.user == mailing.user


from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from functools import wraps


def login_and_author_required(view_func):
    """
    Декоратор для проверки, что пользователь авторизован
    и является автором объекта.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Проверка авторизации
        if not request.user.is_authenticated:
            raise PermissionDenied("Вы должны быть авторизованы.")

        # Получение объекта из модели Wishlist
        obj = get_object_or_404(Wishlist, pk=kwargs.get('pk'))

        # Проверка на авторство
        if obj.creator != request.user:
            raise PermissionDenied("Вы не являетесь автором этого объекта.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
