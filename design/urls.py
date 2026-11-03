from django.urls import path
from .views import BBLoginView, BBLogoutView

urlpatterns = [
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
]