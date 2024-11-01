from django.urls import path
from wishlist.apps import WishlistConfig
from wishlist.views import WishlistListView, WishlistDetailView, WishlistCreateView, WishlistUpdateView, \
    WishlistDeleteView

app_name = WishlistConfig.name

urlpatterns = [
    path('', WishlistListView.as_view(), name='main'),
    path('list/', WishlistDetailView.as_view(), name='list_wishlist'),
    path('detail/<int:pk>/', WishlistDetailView.as_view(), name='detail_wishlist'),
    path('create/', WishlistCreateView.as_view(), name='create_wishlist'),
    path('update/<int:pk>/', WishlistUpdateView.as_view(), name='update_wishlist'),
    path('delete/<int:pk>/', WishlistDeleteView.as_view(), name='delete_wishlist'),
]