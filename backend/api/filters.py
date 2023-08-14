from rest_framework.filters import SearchFilter
from django_filters.rest_framework import filters, FilterSet

from recipes.models import Recipe, Ingredient, Tag, Favorite, ShoppingCart


CHOICES_LIST = (
    ('0', 'False'),
    ('1', 'True')
)


class RecipesFilter(FilterSet):
    """"Фильтр для сортировки рецептов."""""
    is_favorited = filters.ChoiceFilter(
        method='is_favorited_method',
        choices=CHOICES_LIST
    )
    is_in_shopping_cart = filters.ChoiceFilter(
        method='is_in_shopping_cart_method',
        choices=CHOICES_LIST
    )
    author = filters.NumberFilter(
        field_name='author',
        lookup_expr='exact'
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    def is_favorited_method(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipe.objects.none()

        favorites = Favorite.objects.filter(user=self.request.user)
        recipes = [item.recipe.id for item in favorites]
        if value == '1':
            return queryset.filter(id__in=recipes)
        if value == '0':
            return queryset.exclude(id__in=recipes)

    def is_in_shopping_cart_method(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipe.objects.none()
        shopping_chart = ShoppingCart.objects.filter(user=self.request.user)
        recipes = [item.recipe.id for item in shopping_chart]
        if value == '1':
            return queryset.filter(id__in=recipes)
        if value == '0':
            return queryset.exclude(id__in=recipes)

    class Meta:
        model = Recipe
        fields = ('author', 'tags')


class IngredientSearchFilter(SearchFilter):
    """Фильтр для поиска ингредиентов по имени"""
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
