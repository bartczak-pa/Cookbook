from django.contrib import admin

from .models import Category, Course, Cuisine, Recipe

# Register your models here.
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Recipe)
admin.site.register(Cuisine)

