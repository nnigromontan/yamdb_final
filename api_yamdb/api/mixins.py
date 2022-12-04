"""Миксины приложения api1."""

from rest_framework import mixins, viewsets


class CreateListDestroyMixinViewset(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    """Кастомный миксин для настройки представлений."""

    pass
