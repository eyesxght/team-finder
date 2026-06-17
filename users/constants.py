from enum import StrEnum


USER_NAME_MAX_LENGTH = 124
USER_SURNAME_MAX_LENGTH = 124
USER_PHONE_MAX_LENGTH = 12
USER_ABOUT_MAX_LENGTH = 256

AVATAR_SIZE = 200
AVATAR_FONT_SIZE = int(AVATAR_SIZE * 0.5)
AVATAR_TEXT_COLOR = 'white'

PAGINATE_BY = 12


class AvatarColor(StrEnum):
    RED = '#F44336'
    PINK = '#E91E63'
    PURPLE = '#9C27B0'
    DEEP_PURPLE = '#673AB7'
    INDIGO = '#3F51B5'
    BLUE = '#2196F3'
    TEAL = '#009688'
    GREEN = '#4CAF50'
    ORANGE = '#FF9800'
    BROWN = '#795548'


AVATAR_COLORS = [
    AvatarColor.RED,
    AvatarColor.PINK,
    AvatarColor.PURPLE,
    AvatarColor.DEEP_PURPLE,
    AvatarColor.INDIGO,
    AvatarColor.BLUE,
    AvatarColor.TEAL,
    AvatarColor.GREEN,
    AvatarColor.ORANGE,
    AvatarColor.BROWN,
]
