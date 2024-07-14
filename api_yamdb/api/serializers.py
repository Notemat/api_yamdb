from datetime import datetime
from django.db.models import Avg
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
import re

from rest_framework import serializers

from reviews.models import (Category,
                            Comment,
                            Genre,
                            GenreTitle,
                            Review,
                            Title,
                            User
                            )


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
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate(self, data):
        if 'year' in data and data['year'] > datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего.'
            )
        return data

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            GenreTitle.objects.create(
                title=title, genre=genre
            )
        return title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')

    def validate_score(self, value):
        """Проверка, что оценка находится в диапазоне от 1 до 10."""
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                "Оценка должна быть в диапазоне от 1 до 10."
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
        read_only_fields = ('id', 'author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""

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
        validators = [
            EmailValidator,
            RegexValidator(
                regex=r'^[\w.@+-]',
                message='Недопустимый никнейм',
            )
        ]

    def validate_username(self, value):
        """Валидация имени пользователя."""
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise ValidationError('Недопустимый никнейм.')
        if value.lower() == 'me':
            raise ValidationError('Имя пользователя "me" запрещено.')
        return value

    def validate_email(self, value):
        """Проверка валидности email."""
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", value):
            raise ValidationError("Неверный формат email.")
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для токена."""

    username = serializers.SlugField(max_length=150, required=True)

    class Meta:
        """Мета класс токена."""

        fields = '__all__'
        model = User


class InitialRegisterDataSerializer(serializers.Serializer):
    """Сериализатор входящих данных пользователя."""

    username = serializers.CharField()
    email = serializers.EmailField()


class RegisterDataSerializer(serializers.ModelSerializer):
    """Сериализатор для данных регистрации."""

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise ValidationError('Недопустимый никнейм.')
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать \'me\' в качестве логина')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True, source='genre')
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
