from django.db import models
from django.contrib.auth.models import User


class FavoriteRecipes(models.Model):
    user = models.ManyToManyField(User)
    title = models.CharField(max_length=200, verbose_name="title")
    image = models.CharField(max_length=200, verbose_name="image")
    recipe_url = models.CharField(max_length=300, verbose_name="recipe_url")