from django.conf import settings
from django.shortcuts import redirect

from urllib.parse import urlencode
import requests
import json


# used to append url parameters when redirecting users.
def RedirectParams(**kwargs):
    url = kwargs.get("url")
    params = kwargs.get("params")
    response = redirect(url)
    if params:
        query_string = urlencode(params)
        response['Location'] += '?' + query_string
    return response

class APIMixin:

    def __init__(self, *args, **kwargs):
        self.query = kwargs.get("query")

    def get_data(self):

        url = f"https://api.spoonacular.com/recipes/complexSearch?query={self.query}&addRecipeInformation=true&number=10&apiKey={settings.API_KEY}"

        r = requests.get(url)
        if r.status_code == 200:
            try:
                return r.json()["recipes"]
            except KeyError:
                return r.json()['results']
        else:
            return None

# spoonacular APIのポイントの消費が激しいのでコメントアウトしました（新しい方法を見つけました！）
# def get_recipe_detail(self):
#     detail_url = f"https://api.spoonacular.com/recipes/{self}/information?includeNutrition=false&apiKey={settings.API_KEY}"
#     detail_r = requests.get(detail_url)
#     # try:
#     return detail_r.json()["sourceUrl"]
#     # except:
#     #     return None

def random_recipes(self):
    random_recipes_url = f"https://api.spoonacular.com/recipes/random?number={self}&apiKey={settings.API_KEY}" # ランダムなレシピを取得する
    random_recipes_r = requests.get(random_recipes_url)

    if random_recipes_r.status_code == 200:
        return random_recipes_r.json()["recipes"]