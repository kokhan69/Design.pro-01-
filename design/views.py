from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.core.signing import BadSignature
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import RegisterForm, ApplicationForm, AdminApplicationForm
from .models import AdvUser, Application
from .utilities import signer

from django.core.exceptions import PermissionDenied

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

@login_required
def application_create(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('profile')
    else:
        form = ApplicationForm()

    return render(request, 'design/application_create.html', {'form': form})

@login_required
def profile(request):
    applications = Application.objects.filter(user=request.user)
    context = {'applications': applications}
    return render(request, 'design/profile.html', context)

class ApplicationDeleteView(DeleteView):
    model = Application
    template_name = 'design/application_delete.html'
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user or obj.status != 'new':
            raise PermissionDenied("Вы не можете удалить эту заявку.")
        return super().dispatch(request, *args, **kwargs)

class AdminApplicationUpdateView(UserPassesTestMixin, UpdateView):
    model = Application
    form_class = AdminApplicationForm
    template_name = 'design/admin_application_update.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        return self.request.user.is_staff