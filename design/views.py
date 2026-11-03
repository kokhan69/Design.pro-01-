from django.contrib.auth.views import LoginView, LogoutView

class BBLoginView(LoginView):
    template_name = 'design/login.html'

class BBLogoutView(LogoutView):
    next_page = 'index'