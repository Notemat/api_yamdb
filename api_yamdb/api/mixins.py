import re

from django.core.exceptions import ValidationError
from rest_framework import serializers, status
from rest_framework.response import Response

from reviews.constants import USERNAME_MAX_LENGTH
from reviews.models import User


class NotAllowedPutMixin:
    """Миксин, запрещающий 'PUT'-запросы."""

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class ValidateUsernameMixin:
    """Миксин для валидации имени пользователя."""

    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)

    def validate_username(self, value):
        """Валидация имени пользователя."""
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise ValidationError('Недопустимый никнейм.')
        if value == 'me':
            raise ValidationError('Имя пользователя "me" запрещено.')
        if User.objects.filter(username=value).exists():
            raise ValidationError('Данный username уже используется.')
        return value
    
