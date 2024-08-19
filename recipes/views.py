from django.shortcuts import render


def home(request) -> render:  # noqa: ANN001
    return render(request, "recipes/home.html")
