from django.contrib import admin

from .models import Category, Course, Cuisine, Ingredient, Instruction, NutritionalInfo, Recipe, Timing

# Register your models here.
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Recipe)
admin.site.register(Cuisine)
admin.site.register(Instruction)
admin.site.register(Ingredient)
admin.site.register(Timing)
admin.site.register(NutritionalInfo)



