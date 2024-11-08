from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from reviews.forms import (
    AdminUserCreationForm, AdminTitleForm, AdminUserChangeForm)
from reviews.models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserCreationForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    search_fields = ('username',)
    list_editable = ('role',)
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
    form = AdminTitleForm
    list_display = ('name', 'year', 'get_genres')
    search_fields = ('name',)
    list_filter = ('year',)

    @admin.display(
        description='Жанры',
    )
    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date')
    search_fields = ('title__name', 'author__username',)
    list_filter = ('pub_date',)
    fieldsets = (
        (None, {
            'fields': (('title', 'author', 'score'), 'text'),
        }),
    )


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'pub_date')
    search_fields = ('author__username',)
    list_filter = ('pub_date',)
    fieldsets = (
        (None, {
            'fields': (('review', 'author'), 'text'),
        }),
    )
