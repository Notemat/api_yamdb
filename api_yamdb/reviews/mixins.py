from django.db import models

from reviews.constants import LENGTH_TO_DISPLAY


class CategoryGenreMixin(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:LENGTH_TO_DISPLAY]
