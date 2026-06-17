from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .constants import (
    USER_ABOUT_MAX_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_PHONE_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
)
from .managers import UserManager
from .services import generate_avatar


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    name = models.CharField('Имя', max_length=USER_NAME_MAX_LENGTH)
    surname = models.CharField('Фамилия', max_length=USER_SURNAME_MAX_LENGTH)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True)
    phone = models.CharField('Телефон', max_length=USER_PHONE_MAX_LENGTH, unique=True)
    github_url = models.URLField('Github', blank=True)
    about = models.TextField('О себе', blank=True, max_length=USER_ABOUT_MAX_LENGTH)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    favorites = models.ManyToManyField(
        'projects.Project',
        blank=True,
        related_name='interested_users',
        verbose_name='Избранные проекты',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def save(self, *args, **kwargs):
        if not self.avatar and self.name:
            self.avatar = generate_avatar(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.surname}'

    def get_full_name(self):
        return f'{self.name} {self.surname}'

    def get_short_name(self):
        return self.name
