from django import forms

from wishlist.models import Wishlist


class WishlistForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        creator = kwargs.pop('creator', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Wishlist
        fields = ('title', 'description', 'image', 'url', 'price', 'visibility', 'is_active')