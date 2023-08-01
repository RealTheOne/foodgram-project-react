from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Follow, Ingredient, Recipe, RecipeIngredient, Tag
from users.models import User


class TagSerializer(serializers.ModelSerializer):
    """Tag serializer."""

    class Meta:
        model = Tag
        fields = '__all__'


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    """Recipe ingredient serializer."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe serializer."""

    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientsSerializer(
        many=True, source='ingredient'
    )

    class Meta:
        model = Recipe
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Ingredient serializer."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class CustomUserSerializer(UserSerializer):
    """Custom user serializer."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return Follow.objects.filter(
            author=obj,
            user=self.context.get('request').user
        ).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Custom user create serializer."""

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )


class RecipeListSerializer(serializers.ModelSerializer):
    """Recipe list serializer."""

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientsSerializer(many=True, source='ingredient')
    is_favorited = serializers.BooleanField(
        default=False, read_only=True, source='favored'
    )
    is_in_shopping_cart = serializers.BooleanField(
        default=False, read_only=True, source='shoppings'
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )


class CreateIngredientSerializer(serializers.ModelSerializer):
    """Create ingredient serializer."""

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Recipe create serializer."""

    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = CreateIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def validate(self, data):
        name = data.get('name')
        if len(name) > 200:
            raise serializers.ValidationError(
                'Recipe name is more than 200 symbols.'
            )
        ingredients = data.get('ingredients')
        ingredients_list = [ingredient.get('id') for ingredient in ingredients]
        count = Ingredient.objects.count()
        for ingredient in ingredients:
            if ingredient.get('id') > count:
                raise serializers.ValidationError(
                    'There is no such ingredient.'
                )
            if ingredients_list.count(ingredient['id']) > 1:
                double = Ingredient.objects.get(
                    pk=ingredient.get('id')
                )
                raise serializers.ValidationError(
                    f'Ingredient, {double}, '
                    f'picked more than once.'
                )
            if ingredient.get('amount') <= 0:
                zero = Ingredient.objects.get(
                    pk=ingredient.get('id')
                )
                raise serializers.ValidationError(
                    f'Ingredient, {zero}, '
                    f'is 0 or less.'
                )
        return data

    def create_ingredients(self, recipe, ingredients):
        ingredients_list = []
        for ingredient in ingredients:
            create_ingredients = RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
            ingredients_list.append(create_ingredients)
        RecipeIngredient.objects.bulk_create(ingredients_list)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        if 'tags' in validated_data:
            tags = validated_data.get('tags')
            instance.tags.set(tags)
        if 'ingredients' in validated_data:
            instance.ingredients.clear()
            self.create_ingredients(
                instance, validated_data.get('ingredients')
            )
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeListSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data


class SubscribeRecipeSerializer(serializers.ModelSerializer):
    """Subscribe recipe serializer."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    """Subscribe serializer."""

    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            author=obj.author, user=obj.user
        ).exists()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.author)
        return SubscribeRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


class SubscribeUserSerializer(serializers.ModelSerializer):
    """Subscribe user serializer."""

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author',),
                message='You are already subscribed.'
            )
        ]

    def validate(self, data):
        if data.get('user') == data.get('author'):
            raise serializers.ValidationError(
                'You cannot subscribe to yourself.'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return SubscribeSerializer(
            instance, context={'request': request}
        ).data
