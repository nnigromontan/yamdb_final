"""Модели приложения reviews."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validators import year_validator

CHOICES = ((10, 'Best'),
           (9, 'Perfect'),
           (8, 'Excellent'),
           (7, 'Great'),
           (6, 'Good'),
           (5, 'Normal'),
           (4, 'Bad'),
           (3, 'Poor'),
           (2, 'Terrible'),
           (1, 'Worst'))


class Category(models.Model):
    """Описание модели Category."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        """Класс Meta, хранящий дополнительную информацию о модели Category."""

        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        """Возвращает имя объекта."""
        return str(self.name)


class Genre(models.Model):
    """Описание модели Genre."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        """Класс Meta, хранящий дополнительную информацию о модели Genre."""

        ordering = ['name']
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self) -> str:
        """Возвращает имя объекта."""
        return str(self.name)


class Title(models.Model):
    """Описание модели Title."""

    name = models.CharField(max_length=200, db_index=True)
    year = models.IntegerField(
        verbose_name='Year',
        validators=(year_validator,)
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='title related category',
    )
    description = models.TextField(
        blank=True,
        null=True,
        default='default description',
        verbose_name='description',
    )

    genre = models.ManyToManyField(
        Genre,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='title related genre',
    )

    class Meta:
        """Класс Meta, хранящий дополнительную информацию о модели Title."""

        ordering = ['name']
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        """Возвращает имя объекта."""
        return self.name


class Review(models.Model):
    """Описание модели Review."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='reviews author',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='reviews related title',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date of publication',
    )
    text = models.TextField()
    score = models.IntegerField(
        choices=CHOICES,
        validators=[
            MaxValueValidator(10, 'оценка должна быть между 1 и 10'),
            MinValueValidator(1, 'оценка должна быть между 1 и 10'),
        ]
    )

    class Meta:
        """Класс Meta, хранящий дополнительную информацию о модели Review."""

        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class Comment(models.Model):
    """Описание модели Comment."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='comments related review',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='comments author',
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Введите текст комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date of publication',
    )

    class Meta:
        """Класс Meta, хранящий дополнительную информацию о модели Comment."""

        ordering = ['-pub_date']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
