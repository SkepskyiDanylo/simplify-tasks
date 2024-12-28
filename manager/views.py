from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView

from .forms import LoginForm

class UserLoginView(LoginView):
  template_name = "accounts/login.html"
  form_class = LoginForm

class UserLogoutView(LogoutView):
  template_name = "accounts/logged_out.html"