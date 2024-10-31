# Generated by Django 5.1.2 on 2024-10-22 13:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='название желания')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='изображение')),
                ('url', models.URLField(verbose_name='сгсылка на желание')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='цена желания')),
                ('visibility', models.IntegerField(choices=[(0, 'приватный'), (1, 'публичный'), (2, 'только друзья')], verbose_name='Видимость')),
                ('is_completed', models.BooleanField(default=False, verbose_name='признак выполнения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='время обновления')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_wishlists', to=settings.AUTH_USER_MODEL, verbose_name='создатель')),
                ('reserved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reserved_wishlists', to=settings.AUTH_USER_MODEL, verbose_name='признак резервации юзером')),
            ],
        ),
    ]