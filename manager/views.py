from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import LoginForm

class UserLoginView(LoginView):
  template_name = "accounts/login.html"
  form_class = LoginForm