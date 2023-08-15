from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Follow, User

from .filters import IngredientSearchFilter, RecipesFilter
from .pagination import LimitPagePagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    FollowSerializer, IngredientSerializer,
    RecipeCreateSerializer, RecipeForFollowersSerializer,
    RecipeSerializer, TagSerializer, UsersSerializer
)
from recipes.models import (
    AmountIngredients, Favorite, Ingredient,
    Recipe, ShoppingCart, Tag
)


class UsersViewSet(UserViewSet):
    """Вьюсет для модели пользователей"""
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = LimitPagePagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = (
        'username',
        'email'
    )
    permission_classes = (AllowAny, )

    def subscribed(self, serializer, id=None):
        """Создает подписку на автора."""
        follower = get_object_or_404(User, id=id)
        if self.request.user == follower:
            return Response({'message': 'Нельзя подписаться на себя'},
                            status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.get_or_create(user=self.request.user,
                                              author=follower)
        serializer = FollowSerializer(follow[0])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def unsubscribed(self, serializer, id=None):
        """удалет связь между пользователями."""
        follower = get_object_or_404(User, id=id)
        Follow.objects.filter(
            user=self.request.user,
            author=follower
        ).delete()
        return Response({'message': 'Вы успешно отписаны'},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, serializer, id):
        """Создаёт связь между пользователями."""
        if self.request.method == 'DELETE':
            return self.unsubscribed(serializer, id)
        return self.subscribed(serializer, id)

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, serializer):
        """Список подписок пользоваетеля."""
        following = Follow.objects.filter(user=self.request.user)
        pages = self.paginate_queryset(following)
        serializer = FollowSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAuthorOrReadOnly,)


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов"""
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitPagePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        """Метод выбора сериализатора в зависимости от запроса."""
        if self.action == 'list':
            return RecipeSerializer
        if self.action == 'retrieve':
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        """Метод подстановки параметров автора при создании рецепта."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Метод обновления параметров автора при создании рецепта."""
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        """Добавление рецепта в избранное"""
        if request.method == 'POST':
            return self.add_to(Favorite, request.user, pk)
        else:
            return self.delete_from(Favorite, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        """Добавление рецепта в список покупок"""
        if request.method == 'POST':
            return self.add_to(ShoppingCart, request.user, pk)
        else:
            return self.delete_from(ShoppingCart, request.user, pk)

    def add_to(self, model, user, pk):
        """Метод добавления рецепта"""
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({'errors': 'Рецепт уже добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeForFollowersSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        """Метод удаления рецепта"""
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепт уже удален!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        """Загружает файл *.txt co списком покупок."""
        user = request.user
        ingredients = AmountIngredients.objects.filter(
            recipe__shopping_cart__user=user).values(
                'ingredients__name',
                'ingredients__measurement_unit').annotate(
                    amount=Sum('amount'))
        data = ingredients.values_list(
            'ingredients__name',
            'ingredients__measurement_unit',
            'amount'
        )
        shopping_cart = 'Список покупок:\n'
        for name, measure, amount in data:
            shopping_cart += (f'{name} {amount} {measure},\n')
        response = HttpResponse(
            shopping_cart,
            content_type='text/plain'
        )
        return response
