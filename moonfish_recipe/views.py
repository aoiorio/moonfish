from django.shortcuts import render, reverse, redirect
import requests
from django.views import generic
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
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
    # checking if the method is POST
    if request.method == 'POST':
        # getting the recipe name from the form input
        query = request.POST.get("query", None)
        if query:
            results = APIMixin(query=query).get_data()
            if results:
                context = {
                    "results": results,
                    "query": query,
                }
                return render(request, "home/home.html", context) # POSTされて、resultsの中身があったら、contextでresultsとqueryを返す
    else:
        # create recommend_recipes dictionary
        recommend_recipes = {
            "random_recipes": random_recipes(21) # 21個のランダムなレシピを取得
        }
        return render(request, "home/home.html", recommend_recipes) # POSTされなかったら、recommend_recipesを返す
    return render(request, "home/home.html") # これはエラー解消のために書いたもので特に意味はないと思う（絶対にreturnが必要なため）

# favorite page
class FavoritePage(ListView):
    # queryset = Food.objects.filter(is_favorite=True) # favorite itemを表示させるため、querysetでis_favorite=Trueに設定したデータを返す
    template_name = 'favorite/favorite.html'
    context_object_name = "favorite_recipes"
    model = Food