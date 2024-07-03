from django.contrib import admin
from reviews.models import Category, Genre, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')
    search_fields = ('name',)
    list_filter = ('year',)


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    # list_display = ('title', 'author')
    search_fields = ('title', 'author', 'pub_date')
    list_filter = ('pub_date',)
