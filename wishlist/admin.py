from django.contrib import admin
from wishlist.models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'title', 'updated_at','reserved_by', 'is_completed', 'is_active')
    list_filter = ('creator__email', 'is_completed', )
    search_fields = ('creator__email', 'title', 'description', 'reserved_by', )
