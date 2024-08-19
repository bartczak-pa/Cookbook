from django.db import models


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        """Meta definition for Category."""

        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        """Return category name."""
        return self.name


class Course(models.Model):
    """Model definition for Course."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        """Meta definition for Course."""

        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self) -> str:
        """Return course name."""
        return self.name
