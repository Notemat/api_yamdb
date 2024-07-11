from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import generics, viewsets, status
from rest_framework.filters import SearchFilter


from reviews.models import Category, Genre, Review, Title, User
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    MeSerializer,
    TokenSerializer,
    UserSerializer
)
from api.mixins import NotAllowedPutMixin
from api.permissions import (
    IsAdminPermission,
    IsAuthorOrModeratorOrAdminPermission
)


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """list and create для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminPermission, )
    filter_backends = (SearchFilter, )
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
    filter_backends = (SearchFilter, )
    search_fields = ('name', )


class GenreDestroyAPIView(generics.DestroyAPIView):
    """delete для объекта модели Genre."""

    serializer_class = GenreSerializer
    permission_classes = (IsAdminPermission, )

    def get_queryset(self):
        queryset = get_object_or_404(Genre, slug=self.kwargs['slug'])
        return queryset


# возможно нехватает каких-то методов, например доп валидации
class TitleViewSet(NotAllowedPutMixin, viewsets.ModelViewSet):
    """CRUD для модели Title."""

    queryset = Title.objects.prefetch_related('genre', 'category')
    permission_classes = (IsAdminPermission, )
    filter_backends = (SearchFilter, )
    search_fields = ('name', 'year', 'category__slug', 'genre__slug')

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(NotAllowedPutMixin, viewsets.ModelViewSet):
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


class CommentViewSet(NotAllowedPutMixin, viewsets.ModelViewSet):
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
        return self.get_review_object().comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review_object()
        )


@api_view(['POST'])
def send_confirmation_code(request):
    """Функция для получения кода."""
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    try:
        user = User.objects.get(email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'{confirmation_code}',
            f'{settings.ADMIN_EMAIL}',
            [f'{email}'],
            fail_silently=False,
        )
        return Response(
            {'message': 'Пользователь уже существует'},
            status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        user = User.objects.create(
            email=email,
            username=username
        )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения',
        f'{confirmation_code}',
        f'{settings.ADMIN_EMAIL}',
        [f'{email}'],
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


class UserViewSet(viewsets.ModelViewSet):
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
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = MeSerializer(user)
            return Response(serializer.data)
