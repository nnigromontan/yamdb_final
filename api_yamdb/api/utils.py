"""Инструменты приложения api."""

from rest_framework import serializers


def check_username_not_me(value):
    """Валидатор username."""
    if value.lower() == 'me':
        raise serializers.ValidationError(
            'Нельзя назвать пользователя "me"!'
        )
    return value
