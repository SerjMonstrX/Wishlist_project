from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from wishlist.forms import WishlistForm
from wishlist.models import Wishlist
from wishlist.permissions import LoginANdAuthorRequiredMixin, login_and_author_required


class HomeView(ListView):
    model = Wishlist
    template_name = 'wishlist/home_wishlist.html'

    def get_queryset(self, *args, **kwargs):
        # Получаем базовый queryset
        queryset = super().get_queryset()

        # Фильтруем по активным объектам
        queryset = queryset.filter( is_active=True).order_by('updated_at')

        return queryset


class WishlistPersonalPage(ListView):
    model = Wishlist
    template_name = 'wishlist/personal_page_wishlist.html'

    def get_queryset(self, *args, **kwargs):
        # Получаем базовый queryset
        queryset = super().get_queryset()

        # Фильтруем по текущему пользователю и активным объектам
        queryset = queryset.filter(creator=self.request.user).order_by('updated_at')

        return queryset


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
    if wish_item.is_active:
        wish_item.is_active = False
    else:
        wish_item.is_active = True

    wish_item.save()

    return redirect(reverse('wishlist:personal_page_wishlist'))
