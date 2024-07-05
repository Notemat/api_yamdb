from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import generics

from reviews.models import Category, Genre, Review, Title
from api.serializers import CategorySerializer, GenreSerializer, ReviewSerializer


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
        return self.get_title_object().reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title_object()
        )


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """list and create для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes


class CategoryDestroyAPIView(generics.DestroyAPIView):
    """delete для объекта модели Category."""

    serializer_class = CategorySerializer
    # permission_classes

    def get_queryset(self):
        queryset = get_object_or_404(Category, slug=self.kwargs['slug'])
        return queryset


class GenreListCreateAPIView(generics.ListCreateAPIView):
    """list and create для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes


class GenreDestroyAPIView(generics.DestroyAPIView):
    """delete для объекта модели Genre."""

    serializer_class = GenreSerializer
    # permission_classes

    def get_queryset(self):
        queryset = get_object_or_404(Genre, slug=self.kwargs['slug'])
        return queryset
