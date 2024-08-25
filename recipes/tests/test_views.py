import pytest
from django.http import Http404
from django.test import RequestFactory
from django.urls import reverse

from recipes.models import Category, Cuisine, Ingredient, Instruction, Recipe
from recipes.views import RecipeDetailView


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
            cuisine=self.cuisine,  # Associate the cuisine
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
        ids=["valid_recipe", "another_valid_recipe"],
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
        ids=["non_existent_recipe", "non_existent_category"],
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
        view.kwargs = {"slug": "chocolate-cake", "category_slug": "desserts"}  # Ensure kwargs is set

        # Act
        queryset = view.get_queryset()

        # Assert
        assert queryset.model == Recipe
        assert queryset.prefetch_related("ingredients", "instructions").exists()

    def test_get_context_data(self, setup: None) -> None:
        # Arrange
        request = self.factory.get(
            reverse("recipe_detail", kwargs={"slug": "chocolate-cake", "category_slug": "desserts"}))
        view = RecipeDetailView()
        view.request = request
        view.object = self.recipe
        view.kwargs = {"slug": "chocolate-cake", "category_slug": "desserts"}  # Ensure kwargs is set

        # Act
        context = view.get_context_data()

        # Assert
        assert "instructions" in context
        assert list(context["instructions"]) == list(self.recipe.instructions.all())
