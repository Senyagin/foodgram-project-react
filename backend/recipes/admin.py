from django.contrib import admin

from .models import (
    Favorite, Ingredient, Recipe,
    AmountIngredients, ShoppingCart, Tag
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Панель администратора для модели тэгов"""
    list_display = (
        'id',
        'name',
        'slug',
        'color'
    )
    list_filter = (
        'name',
        'slug'
    )
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Панель администратора для модели ингредиентов"""
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    list_filter = (
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Панель администратора для модели рецептов"""
    list_display = (
        'name',
        'author',
        'count_favorites',
        'pub_date',
    )
    list_filter = (
        'author',
        'name',
        'tags'
    )
    search_fields = (
        'name',
        'author__username',
        'tags__name'
    )

    def count_favorites(self, obj: Recipe):
        return obj.favorite.count()


@admin.register(AmountIngredients)
class AmountIngredientstAdmin(admin.ModelAdmin):
    """Панель администратора для модели описывающую
       количество игредиентов в рецепте."""
    list_display = (
        'id',
        'recipe',
        'ingredients',
        'amount'
    )
    list_filter = (
        'recipe',
        'ingredients',
        'amount'
    )
    search_fields = (
        'recipe__name',
        'ingredients__name'
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Панель администратора для модели избранного"""
    list_display = (
        'id',
        'recipe',
        'user'
    )
    list_filter = (
        'recipe',
        'user'
    )
    search_fields = (
        'recipe__name',
        'user__username'
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Панель администратора для модели списка покупок"""
    list_display = (
        'id',
        'recipe',
        'user'
    )
    list_filter = (
        'recipe',
        'user'
    )
    search_fields = (
        'recipe__name',
        'user__username'
    )
