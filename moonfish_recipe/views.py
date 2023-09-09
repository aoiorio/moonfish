from django.shortcuts import render, reverse, redirect, get_object_or_404, HttpResponseRedirect
import requests
from django.views import generic
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
# Userがログインしているかどうかを見極めるデコレータ
from django.contrib.auth.decorators import login_required

# modelsからのimport
from .models import Food

from .mixins import (
        RedirectParams,
        APIMixin,
        random_recipes
)
class SignupPage(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('moonfish_recipe:login')
    template_name = 'registration/signup.html'


@login_required(login_url='moonfish_recipe:login')
def home(request):
    # food = get_object_or_404(Food, id=id)
    # is_favorite = False

    # if food.favorites.filter(id=request.user.id).exists():
    #     is_favorite = True

    # checking if the method is POST
    if request.method == 'POST':
        # getting the recipe name from the form input
        query = request.POST.get("query", None)
        if query:
            results = {}
            food_obj = []
            query_results = APIMixin(query=query).get_data()
            # APIを叩いて取得したデータをfor文で回して、Food DBのtitleに引っかかるものをfood_objに格納する            
            if query_results:
                for item in query_results:
                    food_obj.append(Food.objects.filter(title=item['title']))
                results = food_obj

            if results:
                context = {
                    "results": results,
                    "query": query,
                }
                return render(request, "home/home.html", context) # POSTされて、resultsの中身があったら、contextでresultsとqueryを返す
    else:
        random_recipes_obj = []
        for item in random_recipes(21):
            random_recipes_obj.append(Food.objects.filter(title=item['title']))
        random_recipes_results = random_recipes_obj

        # create recommend_recipes dictionary
        recommend_recipes = {
            "random_recipes_results": random_recipes_results, # 21個のランダムなレシピを取得
        }
        return render(request, "home/home.html", recommend_recipes) # POSTされなかったら、recommend_recipesとis_favoriteを返す

    return render(request, "home/home.html") # これはエラー解消のために書いたもので特に意味はないと思う（絶対にreturnが必要なため）

# add favorite
def add_or_remove_favorite(request, id):
    recipe = get_object_or_404(Food, id=id) # 値を取得している

    if recipe.favorites.filter(id=request.user.id).exists():
        recipe.favorites.remove(request.user)
    else:
        recipe.favorites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# favorite page
def favorites_list(request):
    user_favorites_list = Food.objects.filter(favorites=request.user)
    return render(request, 'favorite/favorite.html', {'user_favorite_list': user_favorites_list})