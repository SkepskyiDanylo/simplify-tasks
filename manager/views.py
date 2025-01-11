from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView, CreateView, UpdateView, TemplateView, DeleteView

from .forms import LoginForm, WorkerSearchForm, WorkerForm, TaskSearchForm, TaskForm, TaskProjectForm
from .models import Worker, Task, Project, Team


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm


class UserLogoutView(LogoutView):
    template_name = "accounts/logged_out.html"


class IndexView(TemplateView):
    template_name = "manager/index.html"

    def get_context_data(self, **kwargs):
        tasks_completed = round(Task.objects.filter(is_completed=True).count() / Task.objects.count() * 100)
        tasks_not_completed = round(Task.objects.filter(is_completed=False).count() / Task.objects.count() * 100)
        month = timezone.now().month
        tasks_this_month = Task.objects.filter(is_completed=True, completed_at__month=month).count()
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.filter(is_completed=True).order_by("-completed_at")[:6]
        context["workers_count"] = Worker.objects.count()
        context["tasks_count"] = Task.objects.count()
        context["tasks_completed"] = tasks_completed
        context["tasks_not_completed"] = tasks_not_completed
        context["tasks_completed_rounded"] = round(tasks_completed / 10) * 10
        context["tasks_not_completed_rounded"] = round(tasks_not_completed / 10) * 10
        context["tasks_this_month"] = tasks_this_month
        context["projects_count"] = Project.objects.count()
        context["teams_count"] = Team.objects.count()
        context["segment"] = "home page"
        return context


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
            if status == "Online":
                queryset = queryset.filter(is_online=True)
            elif status == "Offline":
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = f"worker #{self.object.pk} edit"
        return context


class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "manager/task_list.html"
    paginate_by = 8

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["segment"] = "tasks"
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Task.objects.all().filter(project=None)
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class TaskDetailView(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "manager/task_detail.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["segment"] = "task"
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Task.objects.all().select_related("project")
        queryset = queryset.prefetch_related("assigners")
        return queryset


def toggle_task_assignment(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    user = request.user
    task = get_object_or_404(Task, pk=pk)
    if user.is_authenticated:
        if user in task.assigners.all():
            task.assigners.remove(user)
        else:
            if task.project:
                if user in task.project.team.workers:
                    task.assigners.add(user)
            else:
                task.assigners.add(user)
    task.save()
    return HttpResponseRedirect(reverse_lazy("manager:task-list"))


def toggle_task_completed(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    user = request.user
    task = get_object_or_404(Task, pk=pk)
    if user.is_authenticated and user in task.assigners.all():
        if task.is_completed:
            task.is_completed = False
            task.completed_at = None
        else:
            task.is_completed = True
            task.completed_at = timezone.now()
    task.save()
    return HttpResponseRedirect(reverse_lazy("manager:task-list"))


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "manager/task_form.html"
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("manager:task-detail", args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = f"task #{self.object.pk} Edit"
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "manager/task_form.html"
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("manager:task-detail", args=[self.object.pk])

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["segment"] = "task create"
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "manager/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("manager:task-list")
