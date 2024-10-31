from django.core.management import BaseCommand

from users.models import User
from wishlist.models import Wishlist


class Command(BaseCommand):

    def handle(self, *args, **options):
        wishlist_list =  [
            {
                    "creator": User.objects.get(pk=1),
                    "title": "Вто222ое желание",
                    "description": "Я хочу комп",
                    "image": "wishlist_images/4f186cf3-4cf7-56b1-8312-27c146693507.jpeg",
                    "url": "https://www.ozon.ru/product/intel-sistemnyy-blok-igrovoy-kompyuter-sl-intel-core-i7-7700-ram-64-gb-ssd-1024-gb-amd-radeon-rx-1721009456/?advert=AOIALF246OVSQ_ag52U2SGl9pumnmv0ZdBB2yGgMItre7I8o4oOakqFU",
                    "price": "61000.00",
                    "visibility": 1,

                }
        ]

        # Пакетное добавление для обращения к БД 1 раз для заполнения всех записей.
        wishes_for_create = []
        for wish_item in wishlist_list:
            wishes_for_create.append(
                Wishlist(**wish_item)
            )

        Wishlist.objects.bulk_create(wishes_for_create)