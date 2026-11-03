from django.urls import path
from .views import BBLoginView, BBLogoutView, RegisterView, RegisterDoneView, user_activate

urlpatterns = [
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/activate/<str:sign>/', user_activate, name='activate'),
]