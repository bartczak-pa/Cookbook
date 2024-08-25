from django.core.exceptions import ValidationError
from django.db import models


def validate_image(image_obj: models.ImageField) -> None:
    """Validate image size and raise ValidationError if it exceeds limit."""
    filesize: int = image_obj.file.size
    megabyte_limit: float = 2.0
    if filesize > megabyte_limit * 1024 * 1024:
        msg: str = f"Max file size is {megabyte_limit}MB"
        raise ValidationError(msg)


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(
        upload_to="category_images/",
        blank=True,
        null=True,
        validators=[validate_image],
        help_text="Maximum file size allowed is 2Mb"
    )

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
    original_link = models.URLField(max_length=255, blank=True)
    image_url = models.URLField(max_length=365, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, related_name="cuisines")
    courses = models.ManyToManyField(Course, related_name="courses")

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

    def __str__(self) -> str:
        return self.title


class NutritionalInfo(models.Model):
    """Model definition for NutritionalInfo."""

    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, related_name="nutritional_info")
    servings = models.IntegerField()
    calories = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "NutritionalInfo"
        verbose_name_plural = "NutritionalInfos"

    def __str__(self) -> str:
        return f"{self.recipe.title} - {self.servings} servings"


class Timing(models.Model):
    """Model definition for TimingInfo."""

    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, related_name="timing_info")
    cook_time = models.DurationField()
    prep_time = models.DurationField()
    total_time = models.DurationField()

    class Meta:
        verbose_name = "TimingInfo"
        verbose_name_plural = "TimingInfos"

    def __str__(self) -> str:
        return f"{self.recipe.title} - {self.total_time}"


class Instruction(models.Model):
    """Model definition for Instruction."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="instructions")
    steps = models.TextField()

    class Meta:
        verbose_name = "Instruction"
        verbose_name_plural = "Instructions"

    def __str__(self) -> str:
        return self.steps


class Ingredient(models.Model):
    """Model definition for Ingredient."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"

    def __str__(self) -> str:
        return f"{self.quantity} of {self.name}"
