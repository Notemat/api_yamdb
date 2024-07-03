from django.db import models


LENGTH_TO_DISPLAY = 25
"""Длина для отображения текста в админке."""


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
    """Модель отзыва."""
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

    def __str__(self):
        return f'Отзыв к произведению {self.title} от автора {self.author}'
