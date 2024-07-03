"""Модели приложения reviews."""

from django.db import models
from django.contrib.auth.models import AbstractUser


LENGTH_TO_DISPLAY = 25
"""Длина для отображения текста в админке."""


class User(AbstractUser):
    """Модель юзера."""

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER_ROLE = [
        ('user', USER),
        ('admin', ADMIN),
        ('moderator', MODERATOR),
    ]

    username = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=100,
        unique=True,
    )
    first_name = models.TextField('Имя', max_length=50, blank=True)
    last_name = models.TextField('Фамилия', max_length=50, blank=True)
    about = models.TextField('О себе', max_length=500, blank=True)
    role = models.CharField(
        'Роль', max_length=30, choices=USER_ROLE, default='user'
    )

    @property
    def is_user(self):
        """Проверка на пользователя."""
        return self.role == self.USER

    @property
    def is_admin(self):
        """Проверка на админа."""
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        """Проверка на модератора."""
        return self.role == self.MODERATOR

    class Meta:
        """Мета класс пользователя."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField('Genre', through='GenreTitle',
                                   verbose_name='Жанр')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 null=True, related_name='titles',
                                 verbose_name='Категория')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:LENGTH_TO_DISPLAY]


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:LENGTH_TO_DISPLAY]


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:LENGTH_TO_DISPLAY]


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    """
    Модель отзыва.
    Доработать после добавления модели пользователя.
    """
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField(verbose_name='Текст')
    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='reviews'
    #     )
    score = models.IntegerField(verbose_name='Оценка')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв к произведению {self.title} от автора {self.author}'
