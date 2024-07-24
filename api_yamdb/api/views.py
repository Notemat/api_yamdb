from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from api.filters import TitlesFilter
from api.mixins import NotAllowedPutMixin
from api.permissions import (IsAdminOrReadPermission, IsAdminPermission,
                             IsAuthorOrModeratorOrAdminPermission)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, RegisterDataSerializer,
                             ReviewSerializer, TitleReadSerializer,
                             TitleWriteSerializer, TokenSerializer,
                             UserSerializer)
from reviews.models import Category, Genre, Review, Title, User


class CategoryGenreCommonViewSet(
    CreateModelMixin, DestroyModelMixin,
    ListModelMixin, viewsets.GenericViewSet
):

    permission_classes = (IsAdminOrReadPermission, )
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreCommonViewSet):
    """list/create/delete для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreCommonViewSet):
    """list/create/delete для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(NotAllowedPutMixin, viewsets.ModelViewSet):
    """CRUD для модели Title."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadPermission, )
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = TitlesFilter
    ordering_fields = ('pk', 'year', 'rating')
    ordering = ('pk')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(NotAllowedPutMixin, viewsets.ModelViewSet):
    """
    Вьюсет для модели отзывов.

    Переопределяем get_queryset для получения title_id и
    perform_create для сохранения автора и произведения.
    """

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthorOrModeratorOrAdminPermission,
        IsAuthenticatedOrReadOnly
    )

    def get_title_object(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title_object().reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title_object()
        )


class CommentViewSet(NotAllowedPutMixin, viewsets.ModelViewSet):
    """
    Вьюсет для модели комментария.
    Переопределяем get_queryset для получения id поста и
    perform_create для сохранения автора и отзыва.
    """

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrModeratorOrAdminPermission,
        IsAuthenticatedOrReadOnly
    )

    def get_review_object(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id, title_id=title_id)

    def get_queryset(self):
        return self.get_review_object().comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review_object()
        )


@api_view(['POST'])
def send_confirmation_code(request):
    """Функция для получения и отправки кода."""
    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения',
        confirmation_code,
        settings.ADMIN_EMAIL,
        [user.email],
        fail_silently=False,
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def send_token(request):
    """Функция для получения токена при отправке кода."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    confirmation_code = request.data.get('confirmation_code')
    refresh = RefreshToken.for_user(user)
    anwser = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    if default_token_generator.check_token(user, confirmation_code):
        AccessToken.for_user(user)
        user.save()
        return Response(anwser)
    return Response(
        {'Error': 'Не совпадает код'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(NotAllowedPutMixin, viewsets.ModelViewSet):
    """Вью-класс для пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, )
    search_fields = ('username', )
    permission_classes = (IsAuthenticated, IsAdminPermission,)
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated, ]
    )
    def me(self, request):
        """Получение или обновление пользователя."""
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['role'] = request.user.role
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
