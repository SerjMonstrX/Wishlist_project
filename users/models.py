from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.models import BaseUserManager

NULLABLE = {'blank': True, 'null': True}


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Установка is_active в True для суперпользователя

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='почта', unique=True)
    is_moderator = models.BooleanField(default=False, verbose_name='Модератор')
    is_active = models.BooleanField(default=False, verbose_name='подтвержден ли аккаунт')
    verification_token = models.CharField(max_length=100, verbose_name='Токен верификации', **NULLABLE)
    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Обновление группы модераторов
        moderators_group, _ = Group.objects.get_or_create(name='moderators')

        if self.is_moderator:
            self.groups.add(moderators_group)
        else:
            self.groups.remove(moderators_group)
