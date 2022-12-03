"""Сериализаторы приложения api."""

from django.utils import timezone
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .utils import check_username_not_me


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки модели User."""

    def validate_username(self, value):
        """Валидатор имени User."""
        return check_username_not_me(value)

    class Meta:
        """Класс Meta, хранящий информацию о полях модели User."""

        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        model = User


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания модели User."""

    def validate_username(self, value):
        """Валидатор имени User."""
        return check_username_not_me(value)

    class Meta:
        """Класс Meta, хранящий информацию полях модели User."""

        fields = ('username', 'email',)
        model = User


class ConfirmUserSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки кодов подтверждения."""

    username = serializers.CharField(max_length=150)

    class Meta:
        """Класс Meta, хранящий информацию полях модели User."""

        fields = ('username', 'confirmation_code',)
        model = User


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки модели Genre."""

    class Meta:
        """Класс Meta, хранящий информацию полях модели Genre."""

        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для обработки модели Category."""

    class Meta:
        """Класс Meta, хранящий информацию полях модели Category."""

        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения объекта модели Title."""

    genre = GenreSerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    rating = serializers.IntegerField()

    class Meta:
        """Класс Meta, хранящий информацию полях модели Title."""

        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category',)


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор для создания объекта модели Title."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        required=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        required=True,
        slug_field='slug'
    )

    class Meta:
        """Класс Meta, хранящий информацию полях модели Title."""

        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category',)
        read_only_fields = ('genre', 'category',)

    def validate_year(self, year):
        """Валидатор года."""
        if year > timezone.now().year:
            raise serializers.ValidationError('Этот год еще не настал.')
        return year


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки объекта модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        """Класс Meta, хранящий информацию полях модели Review."""

        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Валидатор объекта Review."""
        if self.context.get('request').method in ('PATCH',):
            return data
        if Review.objects.filter(
            author=self.context.get('request').user,
            title=self.context.get(
                'request').resolver_match.kwargs.get('title_id')
        ).exists():
            raise serializers.ValidationError(
                'Duplicate review for user {}'
                .format(self.context.get('request').user)
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки объекта модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        """Класс Meta, хранящий информацию полях модели Review."""

        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'review')
