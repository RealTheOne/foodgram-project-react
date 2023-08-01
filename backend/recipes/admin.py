from django.contrib import admin

from .models import (FavoriteRecipe, Follow, Ingredient, Recipe,
                     RecipeIngredient, ShoppingCart, Tag)

EMPTY_VALUE = '-empty-'


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    min_num = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag model administration."""

    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Recipe model administration."""

    inlines = (RecipeIngredientInline,)
    list_display = ('id', 'name', 'author', 'pub_date', 'get_favorite_count',)
    list_filter = ('author__username', 'name', 'tags',)
    search_fields = ('author__username', 'name', 'tags__name',)
    filter_horizontal = ('tags',)
    empty_value_display = EMPTY_VALUE

    def get_favorite_count(self, obj):
        return obj.favorite.count()

    get_favorite_count.short_description = 'Add to favorite'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Ingredient model administration."""

    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Follow model administration."""

    list_display = ('id', 'get_follow',)
    list_filter = ('author',)
    search_fields = ('author__username', 'user__username',)

    def get_follow(self, obj):
        return (f'User {str(obj.user).capitalize()} '
                f'subscribed to {str(obj.author).capitalize()}.')

    get_follow.short_description = 'User subscriptions'


@admin.register(FavoriteRecipe)
class FavoriteAdmin(admin.ModelAdmin):
    """Favorite recipe model administration."""

    list_display = ('id', 'get_favorite',)
    search_fields = ('recipe__name', 'user__username',)

    def get_favorite(self, obj):
        return f'"{obj.recipe}" added by {obj.user}.'

    get_favorite.short_description = 'Favorite recipes'


@admin.register(ShoppingCart)
class ShoppingAdmin(admin.ModelAdmin):
    """Shopping cart model administration."""

    list_display = ('id', 'get_shopping',)
    list_filter = ('recipe',)
    search_fields = ('recipe__name',)

    def get_shopping(self, obj):
        return (f'"{obj.recipe}" added to cart '
                f'by {str(obj.user).capitalize()}.')

    get_shopping.short_description = 'Recipes in shopping cart.'
