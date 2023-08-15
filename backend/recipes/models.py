from django.db import models
from django.core.validators import MinValueValidator

from users.models import User
from recipes.validators import validate_time

MAX_LEN_FIELD = 200
MAX_LEN_COLOR = 7
MAX_LEN_MEASUREMENT = 40


class Tag(models.Model):
    """Модель для тэгов."""
    name = models.CharField(
        'Тэг',
        max_length=MAX_LEN_FIELD,
        unique=True,
    )
    color = models.CharField(
        'Цвет',
        max_length=MAX_LEN_COLOR,
        null=True,
    )
    slug = models.CharField(
        'Слаг тэга',
        max_length=MAX_LEN_FIELD,
        null=True,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name', )

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    """Модель для ингредиентов."""
    name = models.CharField(
        'Ингридиент',
        max_length=MAX_LEN_FIELD,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MAX_LEN_MEASUREMENT,
        help_text='Укажите единицу измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name', )

    def __str__(self):
        return f'{self.name}: {self.measurement_unit}'


class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        'Название',
        max_length=MAX_LEN_FIELD,
    )
    image = models.ImageField('Картинка',)
    text = models.TextField('Описание',)
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Список ингредиентов',
        through='AmountIngredients',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэг',
    )
    cooking_time = models.PositiveSmallIntegerField(validators=[validate_time])
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}'


class AmountIngredients(models.Model):
    """Модель, описывающая количество ингридиентов в рецепте."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='amount_ingredient',
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='amount_ingredient',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=0,
        validators=(MinValueValidator(1,
                    message='Введите количество больше 0.'),)
    )

    class Meta:
        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиентов в рецепте'

    def __str__(self) -> str:
        return f'{self.amount} {self.ingredients}'


class Favorite(models.Model):
    """Модель списка избранного."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingCart(models.Model):
    """Модель списка избранного."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
