from django.urls import path
from .apps import WishlistConfig
from .views import index

app_name = WishlistConfig.name

urlpatterns = [
    path('', index)
]