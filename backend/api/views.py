from api.filters import IngredientSearchFilter
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (CustomUserSerializer, IngredientSerializer,
                             RecipeCreateSerializer, RecipeListSerializer,
                             SubscribeRecipeSerializer, SubscribeSerializer,
                             SubscribeUserSerializer, TagSerializer)
from api.utils import delete, make_shopping_cart, post
from django.db.models import Exists, OuterRef
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from djoser import views
from recipes.models import (FavoriteRecipe, Follow, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Tag)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """List viewset mixin."""


class CustomUserViewSet(views.UserViewSet):
    """Custom user viewset."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Tag viewset."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Recipe viewset."""

    permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly,)

    def get_queryset(self):
        queryset = Recipe.objects.select_related(
            'author'
        ).prefetch_related('tags')
        favorited = self.request.query_params.get('is_favorited')
        shopping_cart = self.request.query_params.get('is_in_shopping_cart')
        author = self.request.query_params.get('author')
        tags = self.request.query_params.getlist('tags')
        if favorited:
            queryset = queryset.filter(favorite__user=self.request.user)
        if shopping_cart:
            queryset = queryset.filter(shopping__user=self.request.user)
        if author:
            queryset = queryset.filter(author=author)
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        if self.request.user.is_authenticated:
            return queryset.annotate(
                favored=Exists(
                    queryset.filter(
                        favorite__user=self.request.user,
                        favorite__recipe=OuterRef('id'),
                    )
                ),
                shoppings=Exists(
                    queryset.filter(
                        shopping__user=self.request.user,
                        shopping__recipe=OuterRef('id'),
                    )
                ),
            )
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            data = post(
                request, pk, Recipe,
                FavoriteRecipe, SubscribeRecipeSerializer
            )
            return Response(data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            return delete(request, pk, Recipe, FavoriteRecipe)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            data = post(
                request, pk, Recipe,
                ShoppingCart, SubscribeRecipeSerializer
            )
            return Response(data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            return delete(request, pk, Recipe, ShoppingCart)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping__user=request.user
        ).values_list(
            'ingredient__name', 'ingredient__measurement_unit', 'amount'
        )
        return FileResponse(
            make_shopping_cart(ingredients),
            as_attachment=True,
            filename='grocery_list.pdf',)


class SubscribeView(APIView):
    """Subscribe and cancel view."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, user_id):
        serializer = SubscribeUserSerializer(
            data={'user': request.user.id, 'author': user_id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data, status=status.HTTP_201_CREATED
        )

    def delete(self, request, user_id):
        follow = get_object_or_404(
            Follow, author=user_id, user=request.user
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsList(ListViewSet):
    """Subscriptions list."""

    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Ingredient viewset."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
