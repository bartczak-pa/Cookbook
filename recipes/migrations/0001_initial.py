# Generated by Django 5.1 on 2024-08-25 12:22

import django.db.models.deletion
import recipes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('image', models.ImageField(blank=True, help_text='Maximum file size allowed is 2Mb', null=True, upload_to='category_images/', validators=[recipes.models.validate_image])),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Cuisine',
                'verbose_name_plural': 'Cuisines',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('original_link', models.URLField(blank=True, max_length=255)),
                ('image_url', models.URLField(blank=True, max_length=365)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.category')),
                ('courses', models.ManyToManyField(related_name='courses', to='recipes.course')),
                ('cuisine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuisines', to='recipes.cuisine')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
            },
        ),
        migrations.CreateModel(
            name='NutritionalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servings', models.IntegerField()),
                ('calories', models.DecimalField(decimal_places=2, max_digits=10)),
                ('recipe', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='nutritional_info', to='recipes.recipe')),
            ],
            options={
                'verbose_name': 'NutritionalInfo',
                'verbose_name_plural': 'NutritionalInfos',
            },
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('steps', models.TextField()),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructions', to='recipes.recipe')),
            ],
            options={
                'verbose_name': 'Instruction',
                'verbose_name_plural': 'Instructions',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.CharField(max_length=50)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.recipe')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
            },
        ),
        migrations.CreateModel(
            name='Timing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cook_time', models.DurationField()),
                ('prep_time', models.DurationField()),
                ('total_time', models.DurationField()),
                ('recipe', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='timing_info', to='recipes.recipe')),
            ],
            options={
                'verbose_name': 'TimingInfo',
                'verbose_name_plural': 'TimingInfos',
            },
        ),
    ]
