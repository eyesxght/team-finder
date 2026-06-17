from django.conf import settings
from django.db import models

from .constants import (
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_STATUS_CHOICES,
    PROJECT_STATUS_MAX_LENGTH,
    ProjectStatus,
)


class Project(models.Model):
    name = models.CharField('Название', max_length=PROJECT_NAME_MAX_LENGTH)
    description = models.TextField('Описание', blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Владелец',
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='participated_projects',
        verbose_name='Участники',
    )
    status = models.CharField(
        'Статус',
        max_length=PROJECT_STATUS_MAX_LENGTH,
        choices=PROJECT_STATUS_CHOICES,
        default=ProjectStatus.OPEN,
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    github_url = models.URLField('Ссылка на Github', blank=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
