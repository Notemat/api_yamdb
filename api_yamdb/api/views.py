from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import generics, viewsets, status

from api.filters import TitlesFilter
from reviews.models import Category, Genre, Review, Title, User
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    InitialRegisterDataSerializer,
    TokenSerializer,
    UserSerializer,
    RegisterDataSerializer
)
from api.mixins import NotAllowedPutMixin
from api.permissions import (
    IsAdminPermission,
    IsAdminOrReadPermission,
    IsAuthorOrModeratorOrAdminPermission
)


class CategoryViewSet(ListModelMixin, CreateModelMixin,
                      DestroyModelMixin, viewsets.GenericViewSet):
    """list/create/delete для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadPermission, )
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreListCreateAPIView(generics.ListCreateAPIView):
    """list and create для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadPermission, )
    filter_backends = (SearchFilter, )
    search_fields = ('name', )


class GenreDestroyAPIView(generics.DestroyAPIView):
    """delete для объекта модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminPermission, )
    lookup_field = 'slug'


class TitleViewSet(NotAllowedPutMixin, viewsets.ModelViewSet):
    """CRUD для модели Title."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('pk')
    permission_classes = (IsAdminOrReadPermission, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
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
    serializer = InitialRegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    if User.objects.filter(username=username, email=email).exists():
        user = User.objects.get(username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'{confirmation_code}',
            f'{settings.ADMIN_EMAIL}',
            [f'{email}'],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user = get_object_or_404(User, username=username, email=email)
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
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if 'role' in request.data:
                raise ValidationError({'role': 'Изменение роли недопустимо'})
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
