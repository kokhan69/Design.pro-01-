from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.core.signing import BadSignature
from django.shortcuts import render, get_object_or_404
from .forms import RegisterForm
from .models import AdvUser
from .utilities import signer

def index(request):
    return render(request, 'design/index.html')

class BBLoginView(LoginView):
    template_name = 'design/login.html'

class BBLogoutView(LogoutView):
    next_page = 'index'

class RegisterView(CreateView):
    model = AdvUser
    template_name = 'design/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register_done')

class RegisterDoneView(TemplateView):
    template_name = 'design/register_done.html'

def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'design/activation_failed.html')

    user = get_object_or_404(AdvUser, username=username)

    if user.is_activated:
        return render(request, 'design/activation_done.html', {'already_activated': True})
    else:
        user.is_active = True
        user.is_activated = True
        user.save()
        return render(request, 'design/activation_done.html', {'already_activated': False})