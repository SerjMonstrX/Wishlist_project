from django.urls import path
from wishlist.apps import WishlistConfig
from wishlist.views import WishlistDetailView, WishlistCreateView, WishlistUpdateView, \
    WishlistDeleteView, toggle_activity, HomeView, WishlistPersonalPage

app_name = WishlistConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home_wishlist'),
    path('list/', WishlistPersonalPage.as_view(), name='personal_page_wishlist'),
    path('detail/<int:pk>/', WishlistDetailView.as_view(), name='detail_wishlist'),
    path('create/', WishlistCreateView.as_view(), name='create_wishlist'),
    path('update/<int:pk>/', WishlistUpdateView.as_view(), name='update_wishlist'),
    path('delete/<int:pk>/', WishlistDeleteView.as_view(), name='delete_wishlist'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity_wishlist'),
]