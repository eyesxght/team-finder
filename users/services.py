import random
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from projects.services import get_paginated_queryset

from .constants import (
    AVATAR_COLORS,
    AVATAR_FONT_SIZE,
    AVATAR_SIZE,
    AVATAR_TEXT_COLOR,
)

__all__ = ['get_paginated_queryset', 'generate_avatar']


def generate_avatar(name):
    """Генерация аватара с первой буквой имени на цветном фоне."""
    color = random.choice(AVATAR_COLORS)
    size = AVATAR_SIZE
    image = Image.new('RGB', (size, size), color)
    draw = ImageDraw.Draw(image)
    letter = (name or '?')[0].upper()

    font = None
    for font_path in (
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        'C:/Windows/Fonts/arial.ttf',
    ):
        try:
            font = ImageFont.truetype(font_path, AVATAR_FONT_SIZE)
            break
        except (IOError, OSError):
            continue

    if font is None:
        font = ImageFont.load_default(size=AVATAR_FONT_SIZE)

    bbox = draw.textbbox((0, 0), letter, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (size - w) / 2 - bbox[0]
    y = (size - h) / 2 - bbox[1]

    draw.text((x, y), letter, fill=AVATAR_TEXT_COLOR, font=font)

    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'{letter.lower()}_avatar.png')
