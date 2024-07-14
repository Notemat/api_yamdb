"""Модели приложения reviews."""
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from reviews.constants import (
    LENGTH_TO_DISPLAY,
    MAX_SCORE_VALUE,
    MIN_SCORE_VALUE,

)
from reviews.mixins import CategoryGenreMixin


class User(AbstractUser):
    """Модель юзера."""

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER_ROLE = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    ]

    max_role_length = max(len(role[1]) for role in USER_ROLE)
    username = models.CharField(
        max_length=150,
        unique=True,
        null=False
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
    )
    bio = models.TextField('О себе', blank=True)
    role = models.CharField(
        'Роль', max_length=max_role_length, choices=USER_ROLE, default='user'
    )

    class Meta:
        """Мета класс пользователя."""

        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        """Проверка на админа."""
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        """Проверка на модератора."""
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(datetime.now().year)],
        verbose_name='Год выпуска'
    )
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField('Genre', through='GenreTitle',
                                   verbose_name='Жанр')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 null=True, related_name='titles',
                                 verbose_name='Категория')

    class Meta:
        ordering = ['year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:LENGTH_TO_DISPLAY]


class Category(CategoryGenreMixin):

    class Meta:
        ordering = ['slug']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreMixin):

    class Meta:
        ordering = ['slug']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    """Модель отзыва."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(MIN_SCORE_VALUE),
            MaxValueValidator(MAX_SCORE_VALUE)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_review'
            )
        ]

    def __str__(self):
        return f'Отзыв к произведению {self.title} от автора {self.author}'


class Comment(models.Model):
    """Модель комментария."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарий'

    def __str__(self):
        return f'Комментарий к отзыву {self.review} от автора {self.author}'
