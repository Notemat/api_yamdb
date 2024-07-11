from rest_framework.response import Response
from rest_framework import status


class NotAllowedPutMixin:
    """Миксин, запрещающий 'PUT'-запросы."""

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)