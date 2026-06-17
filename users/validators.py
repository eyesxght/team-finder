import re
from urllib.parse import urlparse

from django.core.exceptions import ValidationError


def validate_github_url(value):
    """Проверяет, что ссылка ведёт на GitHub."""
    if not value:
        return
    parsed = urlparse(value)
    if not parsed.scheme or 'github.com' not in parsed.netloc.lower():
        raise ValidationError('Ссылка должна вести на Github')


def normalize_phone(value):
    """Нормализует номер телефона к формату +7XXXXXXXXXX."""
    value = value.strip()
    if re.fullmatch(r'\+7\d{10}', value):
        return value
    if re.fullmatch(r'8\d{10}', value):
        return '+7' + value[1:]
    raise ValidationError(
        'Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX'
    )
