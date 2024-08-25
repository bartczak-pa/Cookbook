import pytest
from django.http import Http404
from django.test import RequestFactory
from django.urls import reverse

from recipes.models import Category, Cuisine, Recipe
from recipes.views import CategoryRecipeListView


@pytest.mark.django_db
class TestCategoryRecipeListView:
    @pytest.fixture
    def setup(self, db) -> None:  # noqa: ANN001 Fixture provided by Django
        self.factory = RequestFactory()
        self.category = Category.objects.create(name="Desserts", slug="desserts")
        self.cuisine = Cuisine.objects.create(name="French")  # Create a Cuisine instance
        self.recipe1 = Recipe.objects.create(title="Chocolate Cake", category=self.category, cuisine=self.cuisine)
        self.recipe2 = Recipe.objects.create(title="Apple Pie", category=self.category, cuisine=self.cuisine)

    @pytest.mark.parametrize(
        ("slug", "expected_recipes"),
        [
            ("desserts", ["Chocolate Cake", "Apple Pie"]),
            ("nonexistent", []),  # Expecting an empty list for nonexistent category
        ],
        ids=["valid_category", "invalid_category"],
    )
    def test_get_queryset(self, setup: None, slug: str, expected_recipes: list[str]) -> None:

        # Arrange
        request = self.factory.get(reverse("recipes_by_category", kwargs={"slug": slug}))
        view = CategoryRecipeListView()
        view.request = request
        view.kwargs = {"slug": slug}

        # Act
        queryset = view.get_queryset()
        recipes = list(queryset.values_list("title", flat=True))

        # Assert
        assert recipes == expected_recipes

    @pytest.mark.parametrize(
        ("slug", "expected_category_name"),
        [
            ("desserts", "Desserts"),
            ("nonexistent", None),
        ],
        ids=["valid_category", "invalid_category"],
    )
    def test_get_context_data(self, setup: None, slug: str, expected_category_name: str | None) -> None:

        # Arrange
        request = self.factory.get(reverse("recipes_by_category", kwargs={"slug": slug}))
        view = CategoryRecipeListView()
        view.request = request
        view.kwargs = {"slug": slug}
        view.object_list = view.get_queryset()

        # Act
        if expected_category_name:
            context = view.get_context_data()
            category_name = context["category"].name
        else:
            with pytest.raises(Http404):
                view.get_context_data()  # Single statement inside the context manager
            category_name = None

        # Assert
        assert category_name == expected_category_name
