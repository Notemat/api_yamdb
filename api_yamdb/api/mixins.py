from rest_framework import status
from rest_framework.response import Response


class NotAllowedPutMixin:
    """Миксин, запрещающий 'PUT'-запросы."""

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
