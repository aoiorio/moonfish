from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class SignupPage(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class LobbyPage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'chat/lobby.html'
    # success_url = reverse_lazy('lobby')
    login_url = 'login' # ここのlogin_urlを書かないと、どのurlに飛んだらいいのかがわからなくなるので記述する(エラーになる)

# def lobby(request):
#     return render(request, 'chat/lobby.html') #chat/lobby.htmlのパスが追加されている