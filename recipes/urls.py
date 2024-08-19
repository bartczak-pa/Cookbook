from django.urls import path

from .views import CategoryListView, home

urlpatterns = [
    path("", home, name="home"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
]
