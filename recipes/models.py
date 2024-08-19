from django.db import models


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(max_length=100, unique=True)

    # TODO@pawel: Add image field
    # https://github.com/bartczak-pa/Cookbook/issues/1

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Course(models.Model):
    """Model definition for Course."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Model definition for Recipe."""

    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    original_link = models.URLField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

    def __str__(self) -> str:
        return self.title
