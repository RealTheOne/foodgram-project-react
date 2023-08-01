from rest_framework.filters import SearchFilter


class IngredientSearchFilter(SearchFilter):
    """Ingredient search filter."""

    search_param = 'name'
