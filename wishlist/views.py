from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from users.models import User
from wishlist.forms import WishlistForm
from wishlist.models import Wishlist
from wishlist.permissions import LoginANdAuthorRequiredMixin, login_and_author_required


class HomeView(ListView):
    model = Wishlist
    template_name = 'wishlist/home_wishlist.html'

    def get_queryset(self, *args, **kwargs):
        # Получаем базовый queryset
        queryset = super().get_queryset()

        # Базовый фильтр для видимости
        visibility_filter = [1]  # Для незалогиненных пользователей доступны только публичные желания

        if self.request.user.is_authenticated:
            # Если пользователь залогинен, добавляем фильтр для видимости или владельца
            user = self.request.user
            queryset = queryset.filter(
                Q(visibility__in=[1, 2]) | Q(creator=user)
            )
        else:
            # Для незалогиненных пользователей только публичные желания
            queryset = queryset.filter(visibility__in=visibility_filter)

        # Фильтруем только активные объекты
        queryset = queryset.filter(is_active=True)

        # Упорядочиваем по обновлению
        queryset = queryset.order_by('updated_at')

        return queryset


class WishlistPersonalPage(ListView):
    model = Wishlist
    template_name = 'wishlist/personal_page_wishlist.html'
    context_object_name = 'wishlist'

    def get_queryset(self):
        # Получаем параметр `user_id`, если он передан в URL
        user_id = self.kwargs.get('user_id', None)

        # Если параметр `user_id` передан, то ищем пользователя по id, иначе используем текущего пользователя
        if user_id:
            viewed_user = get_object_or_404(User, id=user_id)
        else:
            viewed_user = self.request.user

        # Фильтруем желания по пользователю
        queryset = super().get_queryset().filter(creator=viewed_user)

        # Если это текущий пользователь, показываем все его желания
        if viewed_user == self.request.user:
            # Без фильтрации по видимости
            return queryset.order_by('updated_at')

        # Если это другой пользователь, показываем только публичные и для друзей желания
        return queryset.filter(visibility__in=[1, 2], is_active=True).order_by('updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id', None)
        if user_id:
            viewed_user = get_object_or_404(User, id=user_id)
        else:
            viewed_user = self.request.user

        # Передаем в контекст информацию о владельце страницы
        context['viewed_user'] = viewed_user
        context['is_owner'] = viewed_user == self.request.user
        return context


class WishlistDetailView(DetailView):
    model = Wishlist
    # template_name = 'wishlist/wishlist_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class WishlistCreateView(LoginRequiredMixin, CreateView):
    model = Wishlist
    form_class = WishlistForm
    # template_name = 'wishlist/wishlist_form.html'
    success_url = reverse_lazy('wishlist:home_wishlist')

    def form_valid(self, form):
        if form.is_valid():
            creator = self.request.user
            form.instance.creator = creator
            new_wish = form.save()
            new_wish.slug = slugify(new_wish.title)
            new_wish.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Получаем ключевые аргументы для формы
        kwargs = super().get_form_kwargs()
        kwargs['creator'] = self.request.user
        return kwargs


class WishlistUpdateView(LoginANdAuthorRequiredMixin, UpdateView):
    model = Wishlist
    form_class = WishlistForm
    # template_name = 'wishlist/wishlist_form.html'
    success_url = reverse_lazy('wishlist:home_wishlist')

    def form_valid(self, form):
        if form.is_valid():
            new_wish = form.save()
            new_wish.slug = slugify(new_wish.title)
            new_wish.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wishlist:detail_wishlist', args=[self.kwargs.get('pk')])


class WishlistDeleteView(LoginANdAuthorRequiredMixin, DeleteView):
    model = Wishlist
    # template_name = 'wishlist/wishlist_confirm_delete.html'
    success_url = reverse_lazy('wishlist:home_wishlist')


@login_and_author_required
def toggle_activity(request, pk):
    wish_item = get_object_or_404(Wishlist, pk=pk)

    # Переключение активности
    wish_item.is_active = not wish_item.is_active
    wish_item.save()

    # Редирект на страницу пользователя, который создал этот элемент
    return redirect(reverse('wishlist:personal_page_wishlist', kwargs={'user_id': wish_item.creator.id}))