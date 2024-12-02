from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()
NULLABLE = {'blank':True, 'null':True }


class Wishlist(models.Model):
    TYPE_CHOICES = (
        (0, 'приватный'),
        (1, 'публичный'),
        (2, 'только друзья'),
    )

    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создатель',
                                related_name='created_wishlists')
    title = models.CharField(max_length=255, verbose_name='название желания')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(verbose_name='изображение', default='wishlist_images/default_image.jpg', upload_to='wishlist_images/', **NULLABLE)
    url = models.URLField(verbose_name='ссылка на желание')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='цена желания', **NULLABLE)
    visibility = models.IntegerField(choices=TYPE_CHOICES, verbose_name='Видимость')
    is_completed = models.BooleanField(default=False, verbose_name='признак выполнения')
    reserved_by = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='признак резервации юзером',
                                    related_name='reserved_wishlists', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='признак активности')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='время обновления')
    views_count = models.IntegerField(default=0, verbose_name='проосмотры')
    slug = models.CharField(max_length=200, verbose_name='slug', **NULLABLE)

    def __str__(self):
        return f'Желание {self.title}'

    class Meta():
        verbose_name = 'Желание'
        verbose_name_plural = 'Желания'
        ordering = ('updated_at', )
