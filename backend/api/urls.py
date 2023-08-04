from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CustomUserViewSet, IngredientViewSet, RecipeViewSet,
                       SubscribeView, SubscriptionsList, TagViewSet)

v1_router = DefaultRouter()
v1_router.register(r'tags', TagViewSet, basename='tags')
v1_router.register(r'users', CustomUserViewSet, basename='users')
v1_router.register(r'recipes', RecipeViewSet, basename='recipes')
v1_router.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path(r'users/subscriptions/', SubscriptionsList.as_view({'get': 'list'})),
    path(r'users/<int:user_id>/subscribe/', SubscribeView.as_view()),
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
