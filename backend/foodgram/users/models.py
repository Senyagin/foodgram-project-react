from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_LEN_FIELD = 150


class User(AbstractUser):
    """Модель для пользователей."""
    username = models.CharField('Уникальный юзернейм',
                                max_length=MAX_LEN_FIELD,
                                blank=False,
                                unique=True,
                                )
    password = models.CharField('Пароль',
                                max_length=MAX_LEN_FIELD,
                                blank=False,
                                )
    email = models.CharField(max_length=254,
                             blank=False,
                             verbose_name='Адрес электронной почты',
                             )
    first_name = models.CharField('Имя',
                                  max_length=MAX_LEN_FIELD,
                                  blank=False,
                                  )
    last_name = models.CharField('Фамилия',
                                 max_length=MAX_LEN_FIELD,
                                 blank=False,
                                 )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}: {self.first_name}'


class Follow(models.Model):
    """Модель для подписчиков."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        def __str__(self):
            return f'{self.user} подписался на {self.author}'
