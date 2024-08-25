import pytest
from django.http import Http404
from django.test import RequestFactory
from django.urls import reverse

from recipes.models import Category, Cuisine, Ingredient, Instruction, Recipe
from recipes.views import CategoryRecipeListView, RecipeDetailView


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

        request = self.factory.get(reverse("recipes_by_category", kwargs={"slug": slug}))
        view = CategoryRecipeListView()
        view.request = request
        view.kwargs = {"slug": slug}

        queryset = view.get_queryset()
        recipes = list(queryset.values_list("title", flat=True))

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

        request = self.factory.get(reverse("recipes_by_category", kwargs={"slug": slug}))
        view = CategoryRecipeListView()
        view.request = request
        view.kwargs = {"slug": slug}
        view.object_list = view.get_queryset()

        if expected_category_name:
            context = view.get_context_data()
            category_name = context["category"].name
        else:
            with pytest.raises(Http404):
                view.get_context_data()  # Single statement inside the context manager
            category_name = None

        # Assert
        assert category_name == expected_category_name


@pytest.mark.django_db
class TestRecipeDetailView:

    @pytest.fixture
    def setup(self) -> None:
        self.factory = RequestFactory()
        self.category = Category.objects.create(name="Desserts", slug="desserts")
        self.cuisine = Cuisine.objects.create(name="French")  # Create a Cuisine instance
        self.recipe = Recipe.objects.create(
            title="Chocolate Cake",
            slug="chocolate-cake",
            category=self.category,
            cuisine=self.cuisine  # Associate the cuisine
        )
        # Create Ingredients
        Ingredient.objects.create(name="Flour", recipe=self.recipe)
        Ingredient.objects.create(name="Sugar", recipe=self.recipe)

        # Create Instructions using the correct field name 'steps'
        Instruction.objects.create(steps="Mix ingredients", recipe=self.recipe)
        Instruction.objects.create(steps="Bake for 30 minutes", recipe=self.recipe)

    @pytest.mark.parametrize(
        ("slug", "category_slug", "expected_title"),
        [
            ("chocolate-cake", "desserts", "Chocolate Cake"),
            ("vanilla-cake", "desserts", "Vanilla Cake"),  # This will not exist
        ],
        ids=["valid_recipe", "another_valid_recipe"]
    )
    def test_get_object(self, setup: None, slug: str, category_slug: str, expected_title: str) -> None:
        # Arrange
        request = self.factory.get(reverse("recipe_detail", kwargs={"slug": slug, "category_slug": category_slug}))
        view = RecipeDetailView()
        view.request = request
        view.kwargs = {"slug": slug, "category_slug": category_slug}

        # Act & Assert
        if slug == "chocolate-cake":
            recipe = view.get_object()
            assert recipe.title == expected_title
        else:
            with pytest.raises(Http404):
                view.get_object()

    @pytest.mark.parametrize(
        ("slug", "category_slug"),
        [
            ("non-existent-recipe", "desserts"),
            ("chocolate-cake", "non-existent-category"),
        ],
        ids=["non_existent_recipe", "non_existent_category"]
    )
    def test_get_object_404(self, setup: None, slug: str, category_slug: str) -> None:
        # Arrange
        request = self.factory.get(reverse("recipe_detail", kwargs={"slug": slug, "category_slug": category_slug}))
        view = RecipeDetailView()
        view.request = request
        view.kwargs = {"slug": slug, "category_slug": category_slug}

        # Act & Assert
        with pytest.raises(Http404):
            view.get_object()

    def test_get_queryset(self, setup: None) -> None:
        # Arrange
        request = self.factory.get(
            reverse("recipe_detail", kwargs={"slug": "chocolate-cake", "category_slug": "desserts"}))
        view = RecipeDetailView()
        view.request = request

        # Act
        queryset = view.get_queryset()

        # Assert
        assert queryset.model == Recipe
        # Check if the queryset is prefetched correctly
        assert queryset.prefetch_related("ingredients", "instructions").exists()

    def test_get_context_data(self, setup: None) -> None:
        # Arrange
        request = self.factory.get(
            reverse("recipe_detail", kwargs={"slug": "chocolate-cake", "category_slug": "desserts"}))
        view = RecipeDetailView()
        view.request = request
        view.object = self.recipe

        # Act
        context = view.get_context_data()

        # Assert
        assert "instructions" in context
        assert list(context["instructions"]) == list(self.recipe.instructions.all())
