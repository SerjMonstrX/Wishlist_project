from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from wishlist.models import Wishlist


class WishlistListView(ListView):
    model = Wishlist
    template_name = 'wishlist/list.html'


class WishlistDetailView(DetailView):
    model = Wishlist
    template_name = 'wishlist/wishlist_detail.html'


class WishlistCreateView(CreateView):
    model = Wishlist
    fields = ('title', 'description', 'image', 'url', 'price', 'visibility')
    template_name = 'wishlist/wishlist_form.html'
    success_url = reverse_lazy('wishlist:index')


class WishlistUpdateView(UpdateView):
    model = Wishlist
    fields = ('title', 'description', 'image', 'url', 'price', 'visibility')
    template_name = 'wishlist/wishlist_form.html'
    success_url = reverse_lazy('wishlist:index')


class WishlistDeleteView(DeleteView):
    model = Wishlist
    template_name = 'wishlist/wishlist_confirm_delete.html'
    success_url = reverse_lazy('wishlist:index')
#

