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


class Cuisine(models.Model):
    """Model definition for Cuisine."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Cuisine"
        verbose_name_plural = "Cuisines"

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


class Content(models.Model):
    """Model definition for Content."""

    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, related_name="recipes")
    cook_time = models.CharField(max_length=50)
    prep_time = models.CharField(max_length=50)
    total_time = models.CharField(max_length=50)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, related_name="recipes")
    servings = models.IntegerField()
    calories = models.DecimalField(max_digits=10, decimal_places=2)
    courses = models.ManyToManyField(Course, related_name="recipes")

    class Meta:
        verbose_name = "Content"
        verbose_name_plural = "Content"

    def __str__(self) -> str:
        return self.recipe.title
