from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import DetailView, ListView

from .forms import LoginForm
from .models import Worker


class UserLoginView(LoginView):
  template_name = "accounts/login.html"
  form_class = LoginForm

class UserLogoutView(LogoutView):
  template_name = "accounts/logged_out.html"


class WorkerListView(ListView):
  model = Worker
  context_object_name = "workers"
  template_name = "manager/worker_list.html"
  paginate_by = 10

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["segment"] = "workers"
    return context


class WorkerDetailView(DetailView):
  model = Worker
  context_object_name = "worker"
  template_name = "manager/profile.html"
  queryset = Worker.objects.all().prefetch_related("teams")

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["segment"] = "profile"
    return context
