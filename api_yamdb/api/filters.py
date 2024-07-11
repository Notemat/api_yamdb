from django_filters import rest_framework as filters

from reviews.models import Title


class TitlesFilter(filters.FilterSet):
    """Фильтр произведений."""
    category = filters.CharFilter(
        field_name='category__slug', lookup_expr='contains')
    genre = filters.CharFilter(
        field_name='genre__slug', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
