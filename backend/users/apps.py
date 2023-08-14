from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Конфигурация для приложения User."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
