from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import SignupPage

app_name = "moonfish_recipe"
urlpatterns = [
    path('', views.home, name='home'), # viewsファイルで追加したlobbyのパスをurlの後ろに何もなかったらlobby.htmlを返す
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignupPage.as_view(), name='signup'),
    path('favorite/<int:id>/', views.favorite_page, name='favorite_page'),
    # path('favorite/', views.favorites_list, name='favorite'),
]