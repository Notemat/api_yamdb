from django.contrib import admin

from reviews.forms import TitleForm
from reviews.models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    search_fields = ('username',)
    fieldsets = (
        (None, {
            'fields': (
                ('is_staff', 'is_active'),
                ('date_joined', 'last_login',),
                ('role', 'is_superuser'),
                'groups',
                'user_permissions',
                ('username', 'password'),
                ('first_name', 'last_name'),
                'bio',
                'email'
            ),
        }),
    )


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
    form = TitleForm
    list_display = ('name', 'year')
    search_fields = ('name',)
    list_filter = ('year',)


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'author', 'pub_date')
    list_filter = ('pub_date',)
    fieldsets = (
        (None, {
            'fields': (('title', 'author', 'score'), 'text'),
        }),
    )


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('review', 'author')
    search_fields = ('review', 'author', 'pub_date')
    list_filter = ('pub_date',)
    fieldsets = (
        (None, {
            'fields': (('review', 'author'), 'text'),
        }),
    )
