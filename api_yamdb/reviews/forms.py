from django import forms

from reviews.models import Genre, Title


class TitleForm(forms.ModelForm):
    """Форма для отображение жанров в модели произведения."""
    genre = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Жанр'
    )

    class Meta:
        model = Title
        fields = '__all__'