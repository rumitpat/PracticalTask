from django.urls import path
from .views import (
    RegisterView,
    profile,

)
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('login-view/', LoginView.as_view(), name='login'),
    path('register-view/', RegisterView.as_view(), name='register'),
    # path('logout-view/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    # path('home/',PostListView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
]
