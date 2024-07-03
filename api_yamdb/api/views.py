from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Review, Title
from api.serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели отзывов.
    Переопределяем get_queryset для получения title_id и
    perform_create для сохранения автора и произведения.
    """
    serializer_class = ReviewSerializer

    def get_title_object(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title_object().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title_object()
        )
