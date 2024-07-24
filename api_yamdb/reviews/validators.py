import re
from datetime import timezone

from django.core.exceptions import ValidationError


def validate_username(self, value):
    """Валидация имени пользователя."""
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError('Недопустимый никнейм.')
    if value == 'me':
        raise ValidationError('Имя пользователя "me" запрещено.')
    return value


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            f'Год выпуска не может быть больше {current_year}.'
        )
