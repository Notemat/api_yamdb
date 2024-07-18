import re
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from reviews.constants import (EMAIL_MAX_LENGTH, MAX_SCORE_VALUE,
                               MIN_SCORE_VALUE, USERNAME_MAX_LENGTH)
from reviews.models import (Category, Comment, Genre, Review,
                            Title, User)


class CategorySerializer(serializers.ModelSerializer):
    """Серилизатор для модели категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения модели произведений."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи модели произведений."""

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
        required=True,
        allow_empty=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    year = serializers.IntegerField(required=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего.'
            )
        return value

    def to_representation(self, instance):
        """Метод для возвращения данных, как при GET запросе."""
        instance.rating = getattr(instance, 'rating', 0)
        serializer = TitleReadSerializer(instance)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        """Проверка, что оценка находится в диапазоне от 1 до 10."""
        if not MIN_SCORE_VALUE <= value <= MAX_SCORE_VALUE:
            raise serializers.ValidationError(
                f'Оценка должна быть в диапазоне от '
                f'{MIN_SCORE_VALUE} до {MAX_SCORE_VALUE}.'
            )
        return value

    def validate(self, data):
        """Проверка на уникальность отзыва пользователя."""
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        if request.method == 'POST':
            if Review.objects.filter(
                title_id=title_id, author=request.user
            ).exists():
                raise serializers.ValidationError(
                    "Вы уже оставили отзыв на это произведение."
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""

    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)

    class Meta:
        """Мета класс пользователя."""

        fields = (
            'bio',
            'email',
            'first_name',
            'last_name',
            'role',
            'username'
        )
        model = User

    def validate_username(self, value):
        """Валидация имени пользователя."""
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise ValidationError('Недопустимый никнейм.')
        if value == 'me':
            raise ValidationError('Имя пользователя "me" запрещено.')
        if User.objects.filter(username=value).exists():
            raise ValidationError('Данный username уже используется.')
        if len(value) > 150:
            raise ValidationError('Имя пользователя не должно превышать 150 символов.')
        return value

    def validate_email(self, value):
        """Проверка валидности email."""
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", value):
            raise ValidationError("Неверный формат email.")
        if User.objects.filter(email=value).exists():
            raise ValidationError('Данный email уже используется.')
        if len(value) > EMAIL_MAX_LENGTH:
            raise ValidationError('Электронная почта не должна превышать 254 символа.')
        return value

    def validate(self, data):
        """Валидация уникальности username и email."""
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username=username, email=email).exists():
            raise ValidationError('Пользователь с такими данными уже существует.')
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для токена."""

    username = serializers.SlugField(
        max_length=USERNAME_MAX_LENGTH,
        required=True
    )
    confirmation_code = serializers.CharField()


class InitialRegisterDataSerializer(serializers.Serializer):
    """Сериализатор входящих данных пользователя."""

    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise ValidationError('Недопустимый никнейм.')
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать \'me\' в качестве логина')
        return value

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        if created:
            user.save()
        return user
