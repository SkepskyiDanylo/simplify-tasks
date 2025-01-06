from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from .forms import LoginForm, WorkerSearchForm, WorkerForm
from .models import Worker, Task


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

  def get_context_data(self, **kwargs) -> dict:
    context = super().get_context_data(**kwargs)
    context["segment"] = "workers"
    username = self.request.GET.get("username", "")
    context["search_form"] = WorkerSearchForm(
      initial={"username": username}
    )
    return context

  def get_queryset(self) -> QuerySet:
    queryset = Worker.objects.all()
    username = self.request.GET.get("username")
    status = self.request.GET.get("status")
    if username:
      queryset = queryset.filter(username__icontains=username)
    if status:
      if status=="Online":
        queryset = queryset.filter(is_online=True)
      elif status=="Offline":
        queryset = queryset.filter(is_online=False)
    return queryset


class WorkerDetailView(DetailView):
  model = Worker
  context_object_name = "worker"
  template_name = "manager/profile.html"
  queryset = Worker.objects.all().prefetch_related("teams")

  def get_context_data(self, **kwargs) -> dict:
    context = super().get_context_data(**kwargs)
    context["segment"] = "profile"
    return context


class WorkerCreateView(LoginRequiredMixin, CreateView):
  model = Worker
  form_class = WorkerForm
  template_name = "manager/worker_form.html"

  def get_success_url(self):
    return reverse_lazy("manager:worker-detail", args=[self.object.pk])

  def get_context_data(self, **kwargs) -> dict:
    context = super().get_context_data(**kwargs)
    context["segment"] = "create worker"
    return context


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
  model = Worker
  template_name = "manager/worker_form.html"
  form_class = WorkerForm

  def get_success_url(self):
    return reverse_lazy("manager:worker-detail", args=[self.object.pk])


class TaskListView(ListView):
  model = Task
  context_object_name = "tasks"
  template_name = "manager/task_list.html"
  paginate_by = 10

  def get_context_data(self, **kwargs) -> dict:
    context = super().get_context_data(**kwargs)
    context["segment"] = "tasks"
    return context