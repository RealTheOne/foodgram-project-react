from django.core.validators import MinValueValidator
from django.db import models

from users.models import User

TEXT_LENGTH = 29


class Tag(models.Model):
    """Tag model."""

    name = models.CharField(
        max_length=200, verbose_name='Name', unique=True
    )
    color = models.CharField(
        max_length=7, verbose_name='Color', unique=True
    )
    slug = models.SlugField(
        max_length=200, verbose_name='Slug', unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Ingredient(models.Model):
    """Ingredient model."""

    name = models.CharField(
        max_length=200, verbose_name='Ingredient name'
    )
    measurement_unit = models.CharField(
        max_length=200, verbose_name='Measurements'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Recipe(models.Model):
    """Recipe model."""

    name = models.CharField(
        max_length=200,
        verbose_name='Recipe name'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Recipe author'
    )
    image = models.ImageField(
        upload_to='recipes/images',
        verbose_name='Recipe image'
    )
    text = models.TextField(
        verbose_name='Recipe text'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Recipe ingredients'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Recipe tag'
    )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Minimal cooking time 1 minute'
            )
        ],
        verbose_name='Cooking time'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Publication date'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class RecipeIngredient(models.Model):
    """Recipe ingredient model."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Ingredient'
    )
    amount = models.IntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Minimal amount no less than 1'
            )
        ],
        verbose_name='Amount'
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Ingredient amount'
        verbose_name_plural = 'Ingredients amount'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient',),
                name='unique_ingredient',
            ),
        ]

    def __str__(self):
        return f'{self.ingredient} in {self.ingredient.measurement_unit}'


class Follow(models.Model):
    """Follow model."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Author'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Follower'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author',),
                name='unique_follow',
            ),
        ]


class FavoriteRecipe(models.Model):
    """Favorite recipe model."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Favorite recipe'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Recipe subscriber'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Favorite recipe'
        verbose_name_plural = 'Favorite recipes'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favorite',
            ),
        ]


class ShoppingCart(models.Model):
    """Shopping cart model."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Recipe for shopping'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Shopping user'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Recipe for shopping'
        verbose_name_plural = 'Recipes for shopping'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_shoppingcart',
            ),
        ]
