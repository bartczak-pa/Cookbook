from django.contrib import admin

from .models import Category, Content, Course, Cuisine, Ingredient, Instruction, Recipe

# Register your models here.
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Recipe)
admin.site.register(Cuisine)
admin.site.register(Content)
admin.site.register(Instruction)
admin.site.register(Ingredient)

