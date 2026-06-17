from urllib.parse import urlparse

from django.core.exceptions import ValidationError


def validate_github_url(value):
    if not value:
        return
    parsed = urlparse(value)
    if not parsed.scheme or 'github.com' not in parsed.netloc.lower():
        raise ValidationError('Ссылка должна вести на Github')
