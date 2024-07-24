from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from reviews.models import Genre, Title, User


class AdminTitleForm(forms.ModelForm):
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


class AdminUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class AdminUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])
