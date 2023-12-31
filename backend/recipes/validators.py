from rest_framework.validators import ValidationError

COOKING_TIME = 1
COUNT_INGREDIENTS = 1


def validate_time(value):
    """Валидация поля модели - время приготовления."""
    if value < COOKING_TIME:
        raise ValidationError(
            [f'Время не может быть менее {COOKING_TIME} минуты']
        )
    return value


def validate_ingredients(data):
    """Валидация ингредиентов и количества."""
    if not data:
        raise ValidationError(['Обязательное поле.'])
    if len(data) < COUNT_INGREDIENTS:
        raise ValidationError(['He переданы ингредиенты.'])
    unique_ingredient = []
    for ingredient in data:
        if not ingredient.get('id'):
            raise ValidationError(
                ['Отсутствует id ингредиента.']
            )
        id = ingredient.get('id')
        if id in unique_ingredient:
            raise ValidationError(
                ['Нельзя использовать один и тот же ингредиент несколько раз']
            )
        unique_ingredient.append(id)
        amount = int(ingredient.get('amount'))
        if amount < 1:
            raise ValidationError(
                ['Количество не может быть менее 1.']
            )
    return data
