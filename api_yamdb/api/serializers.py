from rest_framework import serializers

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывов."""
    author = serializers.SlugRelatedFields(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'title', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'title', 'author', 'pub_date')
