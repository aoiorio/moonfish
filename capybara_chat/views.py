from django.shortcuts import render, reverse, redirect
import requests
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .mixins import (
        FormErrors,
        RedirectParams,
        APIMixin,
        get_recipe_detail,
        random_recipes
)
class SignupPage(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('capybara_chat:login')
    template_name = 'registration/signup.html'

# class LobbyPage(LoginRequiredMixin, generic.TemplateView):
#     template_name = 'chat/lobby.html'
#     # success_url = reverse_lazy('lobby')
#     login_url = 'login' # ここのlogin_urlを書かないと、どのurlに飛んだらいいのかがわからなくなるので記述する(エラーになる)

# def lobby(request):
#     return render(request, 'chat/lobby.html') #chat/lobby.htmlのパスが追加されている
@login_required(login_url='capybara_chat:login')
def home(request):
    # checking if the method is POST
    if request.method == 'POST':
        # getting the recipe name from the form input
        query = request.POST.get("query", None)
        if query:
            return RedirectParams(url = 'capybara_chat:results', params = {"query": query})
    recommend_recipes = {
        "random_recipes": random_recipes(21)
    }
    print(random_recipes)
    return render(request, "home/home.html", recommend_recipes)


def results(request):
        query = request.GET.get("query", None)
        if query:
            results = APIMixin(query=query).get_data()

            if results:
                recipe_urls = []
                for item in results:
                    recipe_urls.append(get_recipe_detail(item['id']))

                for recipe in range(len(recipe_urls)):
                    recipe_url = "recipe_url" + str(recipe)
                    for item in results:
                        item[recipe_url] = recipe_urls[recipe]

                context = {
                    "results": results,
                    "query": query,
                    "recipe_urls": recipe_urls
                }


                return render(request, 'home/results.html', context)

    # the url for recipe, takes query and API_KEY
    # converting the request response to json

        return render(request, "home/home.html")
