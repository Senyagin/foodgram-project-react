from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """Конфигурация для приложения Recipe."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
