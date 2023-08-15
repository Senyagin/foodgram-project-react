from django.contrib import admin

from .models import (
    Favorite, Ingredient, Recipe,
    AmountIngredients, ShoppingCart, Tag
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
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


class IngredientsAmountInline(admin.TabularInline):
    """
    Позволяет выводить кол-во ингредиентов в карточке рецепта через модель
    IngredientsAmount.
    """
    model = AmountIngredients
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'display_tags')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author__username', 'author__last_name',
                     'author__first_name', 'tags__name')
    readonly_fields = ('favorite_count', 'shopping_count')
    filter_vertical = ('tags', 'ingredients')
    inlines = (IngredientsAmountInline,)
    empty_value_display = '--пусто--'

    def favorite_count(self, obj):
        return obj.favorites.count()

    def shopping_count(self, obj):
        return obj.shopcarts.count()

    def display_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])

    favorite_count.short_description = 'В избранном'
    shopping_count.short_description = 'В списке покупок'
    display_tags.short_description = 'Теги'


@admin.register(AmountIngredients)
class AmountIngredientstAdmin(admin.ModelAdmin):
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
