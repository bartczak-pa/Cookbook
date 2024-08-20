from django.urls import path

from .views import CategoryListView, RecipeDetailView, RecipeListView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("", RecipeListView.as_view(), name="recipe_list"),
    path("<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
]
