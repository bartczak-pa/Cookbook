from django.shortcuts import render
from django.views.generic import ListView

from recipes.models import Category


def home(request) -> render:  # noqa: ANN001
    return render(request, "recipes/home.html")


class CategoryListView(ListView):
    model = Category
    context_object_name = "categories"
    queryset = Category.objects.all().order_by("name")
    template_name = "recipes/category_list.html"
    paginate_by = 10
