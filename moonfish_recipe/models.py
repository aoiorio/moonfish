from django.db import models
from django.contrib.auth.models import User

class Food(models.Model):
    title = models.CharField(max_length=100, verbose_name="Recipe_title")
    image = models.CharField(max_length=200, verbose_name="Recipe_image_url")
    recipe_url = models.CharField(max_length=300, verbose_name="Recipe_url")
    # is_favorite = models.BooleanField(default=False, verbose_name="Recipe_is_favorite")
    favorites = models.ManyToManyField(User, related_name="favorites", unique=False)



    # def favoriteObjects(self):
    #     favorite_food = Food.objects.filter(is_favorite=1)
    #     return favorite_food
# class FavoriteRecipes(models.Model):
#     user = models.ManyToManyField(User, primary_key=True)
#     title = models.CharField(max_length=200, verbose_name="title")
#     image = models.CharField(max_length=200, verbose_name="image")
#     recipe_url = models.CharField(max_length=300, verbose_name="recipe_url")
#     is_favorite = models.BooleanField(default=False)