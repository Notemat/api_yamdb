from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.filters import SearchFilter

from reviews.models import Category, Genre, Review, Title
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer
)
from api.permissions import (
    IsAdminPermission,
    IsAuthorOrModeratorOrAdminPermission
)


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """list and create для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminPermission, )
    search_fields = ('name', )


class CategoryDestroyAPIView(generics.DestroyAPIView):
    """delete для объекта модели Category."""

    serializer_class = CategorySerializer
    permission_classes = (IsAdminPermission, )

    def get_queryset(self):
        queryset = get_object_or_404(Category, slug=self.kwargs['slug'])
        return queryset


class GenreListCreateAPIView(generics.ListCreateAPIView):
    """list and create для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminPermission, )
    search_fields = ('name', )


class GenreDestroyAPIView(generics.DestroyAPIView):
    """delete для объекта модели Genre."""

    serializer_class = GenreSerializer
    permission_classes = (IsAdminPermission, )

    def get_queryset(self):
        queryset = get_object_or_404(Genre, slug=self.kwargs['slug'])
        return queryset


# возможно нехватает каких-то методов, например доп валидации
class TitleViewSet(viewsets.ModelViewSet):
    """CRUD для модели Title."""

    queryset = Title.objects.prefetch_related('genre', 'category')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminPermission, )
    search_fields = ('name', 'year', 'category__slug', 'genre__slug')


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели отзывов.
    Переопределяем get_queryset для получения title_id и
    perform_create для сохранения автора и произведения.
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminPermission, )

    def get_title_object(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title_object().reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title_object()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели комментария.
    Переопределяем get_queryset для получения id поста и
    perform_create для сохранения автора и отзыва.
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminPermission, )

    def get_review_object(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        return self.get_post_object().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_review_object()
        )
