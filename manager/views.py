from django.db.models import QuerySet
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import DetailView, ListView

from .forms import LoginForm, WorkerSearchForm
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
