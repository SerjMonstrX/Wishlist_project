# Generated by Django 5.1.2 on 2024-11-03 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0005_wishlist_slug_wishlist_views_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='views_count',
            field=models.IntegerField(default=0, verbose_name='проосмотры'),
        ),
    ]
