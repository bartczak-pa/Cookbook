from django.urls import path

from .views import CategoryListView, CategoryRecipeListView, RecipeDetailView, RecipeListView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/<slug:slug>/", CategoryRecipeListView.as_view(), name="recipes_by_category"),
    path("", RecipeListView.as_view(), name="recipe_list"),
    path("<slug:category_slug>/<slug:slug>/", RecipeDetailView.as_view(), name="recipe_detail"),
]
