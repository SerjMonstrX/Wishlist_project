# Generated by Django 5.1.2 on 2024-11-01 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0003_alter_wishlist_options_alter_wishlist_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='признак активности'),
        ),
    ]
