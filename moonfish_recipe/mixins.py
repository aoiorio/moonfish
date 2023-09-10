from django.conf import settings
from django.shortcuts import redirect
from .models import Food

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

# ユーザーが入れた言葉からレシピ検索をかける
class APIMixin:

    def __init__(self, *args, **kwargs):
        self.query = kwargs.get("query")

    def get_data(self):

        url = f"https://api.spoonacular.com/recipes/complexSearch?query={self.query}&addRecipeInformation=true&number=10&apiKey={settings.API_KEY}"

        r = requests.get(url)

        if r.status_code == 200:
            # データベースにレシピを追加
            for recipe in r.json()["results"]:
                # 同じtitleの要素がDBに入っていたらpassする（要素を追加しない）
                if Food.objects.filter(title=recipe["title"]).exists():
                    pass
                else:
                    foods_obj = Food(title=recipe["title"], image=recipe["image"], recipe_url=recipe["sourceUrl"])
                    foods_obj.save()
            return r.json()["results"]
        else:
            return None

# ランダムなレシピを取得する関数
def random_recipes(self):

    random_recipes_url = f"https://api.spoonacular.com/recipes/random?number={self}&apiKey={settings.API_KEY}"
    random_recipes_r = requests.get(random_recipes_url)

    if random_recipes_r.status_code == 200:
        # Foodsというデータベースにspoonacular APIで取得したデータを格納する
        for recipe in random_recipes_r.json()["recipes"]:
            if Food.objects.filter(title=recipe["title"]).exists(): # 同じtitleの要素がDBに入っていたらpassする（要素を追加しない）
                pass
            else:
                try:
                    foods_obj = Food(title=recipe["title"], image=recipe["image"], recipe_url=recipe["sourceUrl"])
                    foods_obj.save()
                except Exception:
                    foods_obj = Food(title=recipe["title"], image=recipe["image"], recipe_url=recipe["sourceUrl"])
                    foods_obj.save()
        return random_recipes_r.json()["recipes"]