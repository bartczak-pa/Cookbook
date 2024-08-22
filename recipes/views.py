from django.db.models import Count
from django.views.generic import DetailView, ListView

from recipes.models import Category, Recipe


class CategoryListView(ListView):
    model = Category
    context_object_name = "categories"
    queryset = Category.objects.annotate(recipe_count=Count("recipe")).order_by("-recipe_count", "name")
    template_name = "recipes/category_list.html"
    paginate_by = 10


class RecipeListView(ListView):
    model = Recipe
    context_object_name = "recipes"
    queryset = Recipe.objects.all().select_related("timing_info").order_by("title")
    template_name = "recipes/recipe_list.html"
    paginate_by = 15


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = "recipe"
    template_name = "recipes/recipe_detail.html"

    def get_queryset(self) -> Recipe:
        return super().get_queryset().prefetch_related("ingredients", "instructions")

    def get_context_data(self, **kwargs):  # noqa: ANN003, ANN201
        context = super().get_context_data(**kwargs)
        context["instructions"] = self.object.instructions.all()
        return context
