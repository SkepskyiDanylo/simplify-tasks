from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    TemplateView,
    DeleteView
)

from manager.forms import (
    LoginForm,
    WorkerSearchForm,
    WorkerForm,
    TaskSearchForm,
    TaskForm,
    TeamForm,
    ProjectForm
)
from manager.models import (
    Worker,
    Task,
    Project,
    Team
)


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("manager:index"))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        remember_me = self.request.POST.get("rememberMe", False)
        if remember_me:
            self.request.session.set_expiry(3600 * 24 * 7)
        else:
            self.request.session.set_expiry(0)

        return response


class UserLogoutView(LogoutView):
    template_name = "accounts/logged_out.html"


class IndexView(TemplateView):
    template_name = "manager/index.html"

    def get_context_data(self, **kwargs):
        tasks_completed = round(Task.objects.filter(
            is_completed=True
        ).count() / Task.objects.count() * 100)
        tasks_not_completed = round(
            Task.objects.filter(is_completed=False).count()
            / Task.objects.count() * 100)
        month = timezone.now().month
        tasks_this_month = Task.objects.filter(
            is_completed=True,
            completed_at__month=month).count()
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.filter(
            is_completed=True
        ).order_by("-completed_at")[:6]
        context["workers_count"] = Worker.objects.count()
        context["tasks_count"] = Task.objects.count()
        context["tasks_completed"] = tasks_completed
        context["tasks_not_completed"] = tasks_not_completed
        context["tasks_completed_rounded"] = round(tasks_completed / 10) * 10
        context["tasks_not_completed_rounded"] = round(
            tasks_not_completed / 10) * 10
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
    queryset = Worker.objects.all()

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["segment"] = "profile"
        return context

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        user = get_object_or_404(Worker, pk=pk)
        if request.user.is_authenticated and request.user == user:
            return HttpResponseRedirect(reverse("manager:current-profile"))
        return super().get(request, *args, **kwargs)


class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = Worker
    form_class = WorkerForm
    template_name = "manager/worker_form.html"

    def get_success_url(self):
        return reverse_lazy("manager:worker-detail", args=[self.object.pk])

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["segment"] = "create worker"
        context["picture"] = static("/default.jpg")
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
        context["picture"] = get_object_or_404(
            Worker,
            pk=self.object.pk).profile_picture.url
        return context


class ProfileDetailView(LoginRequiredMixin, TemplateView):
    template_name = "manager/profile.html"
    queryset = Worker.objects.all().select_related("team")

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["segment"] = "profile"
        try:
            context["worker"] = Worker.objects.get(pk=self.request.user.pk)
        except Worker.DoesNotExist:
            raise Http404("Profile does not exist")
        return context


class WorkerDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = "manager/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("manager:worker-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "worker delete"
        context["model"] = "worker"
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
        name = self.request.GET.get("name")
        user = self.request.GET.get("user")
        all_tasks = self.request.GET.get("all")
        if all_tasks == "true":
            queryset = Task.objects.all().filter(project=None)
        elif user:
            queryset = Task.objects.all().filter(assigners__in=user)
        else:
            queryset = Task.objects.all().filter(
                project=None,
                is_completed=False
            )
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset.order_by("is_completed", "-completed_at")


class TaskDetailView(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "manager/task_detail.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["segment"] = "task"
        project = self.request.GET.get("project")
        if project:
            context["project"] = Project.objects.get(pk=project)
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Task.objects.all().select_related("project")
        queryset = queryset.prefetch_related("assigners")
        return queryset


@login_required
def toggle_task_assignment(
        request: HttpRequest,
        pk: int) -> HttpResponseRedirect:
    user = request.user
    task = get_object_or_404(Task, pk=pk)
    if user in task.assigners.all():
        task.assigners.remove(user)
    else:
        if task.project:
            if task.project.team and user in task.project.team.workers:
                task.assigners.add(user)
        else:
            task.assigners.add(user)
    task.save()
    return HttpResponseRedirect(reverse_lazy("manager:task-list"))


@login_required
def toggle_task_completed(
        request: HttpRequest,
        pk: int) -> HttpResponseRedirect:
    user = request.user
    task = get_object_or_404(Task, pk=pk)
    if user in task.assigners.all() or user.is_superuser:
        if task.is_completed:
            task.is_completed = False
            task.completed_at = None
        else:
            task.is_completed = True
            task.completed_at = timezone.now()
    task.save()
    project = request.GET.get("project", None)
    if project:
        return HttpResponseRedirect(
            reverse_lazy("manager:project-detail", args=[project])
        )
    return HttpResponseRedirect(reverse_lazy("manager:task-list"))


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "manager/task_form.html"
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("manager:task-detail", args=[self.object.pk])

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context["segment"] = f"task #{self.object.pk} Edit"
        users = list(self.object.assigners.all())
        if user not in users:
            users.append(user)
        context["users"] = users
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
        if self.request.user.is_superuser:
            context["users"] = get_user_model().objects.all()
        else:
            context["users"] = get_user_model().objects.filter(
                pk=self.request.user.pk
            )
        user_id = self.request.GET.get("user", None)
        if user_id:
            try:
                selected_user = get_user_model().objects.get(pk=user_id)
                context["selected_user"] = selected_user
            except User.DoesNotExist:
                pass
        project = self.request.GET.get("project", None)
        if project:
            context["assigned_project"] = Project.objects.get(pk=project)
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "manager/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "task delete"
        context["model"] = "task"
        return context


class ProjectListView(ListView):
    model = Project
    context_object_name = "projects"
    template_name = "manager/project_list.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["segment"] = "projects"
        for project in context["projects"]:
            tasks = project.tasks.all()
            if tasks.count() == 0:
                project.completed_tasks = 0
                project.completed_rounded = 0
            else:
                project.completed_tasks = round(
                    project.tasks.filter(
                        is_completed=True
                    ).count() / project.tasks.all().count() * 100
                )
                project.completed_rounded = round(
                    project.completed_tasks / 10
                ) * 10
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            team = user.team
            if team:
                if user == team.leader:
                    return Project.objects.all()
                return Project.objects.filter(team=team)
        return Project.objects.all()


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = "project"
    template_name = "manager/project_detail.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["segment"] = "project detail"
        return context


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "manager/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("manager:project-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "project delete"
        context["model"] = "project"
        return context


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "manager/project_form.html"

    def get_success_url(self):
        return reverse_lazy("manager:project-detail", args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = f"project #{self.object.pk} Edit"
        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy("manager:project-list"))


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = "manager/project_form.html"
    form_class = ProjectForm

    def get_success_url(self):
        return reverse_lazy("manager:project-detail", args=[self.object.pk])

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["segment"] = "project create"
        return context


class TeamDetailView(DetailView):
    model = Team
    context_object_name = "team"
    template_name = "manager/team_detail.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["segment"] = "team"
        team = context["team"]
        leader = team.leader
        context["workers"] = team.workers.all().exclude(pk=leader.pk)
        return context


@login_required
def add_worker_to_team(request: HttpRequest) -> HttpResponseRedirect | None:
    if request.method == "POST":
        worker_id = int(request.POST.get("worker_id", 0))
        team_id = int(request.POST.get("team_id", 0))

        worker = get_object_or_404(Worker, id=worker_id)
        team = get_object_or_404(Team, id=team_id)
        if request.user == team.leader or request.user.is_superuser:
            worker.team = team
            worker.save()
        return HttpResponseRedirect(
            reverse_lazy("manager:team-detail", kwargs={"pk": team.pk})
        )
    return None


@login_required
def delete_worker_from_team(
        request: HttpRequest,
        **kwargs) -> HttpResponseRedirect:
    user = request.user
    team = get_object_or_404(Team, id=kwargs["pk"])
    if user.is_superuser or user == team.leader:
        del_user = kwargs["user_pk"]
        del_worker = get_object_or_404(Worker, id=del_user)
        team.workers.remove(del_worker)
        team.save()
    return HttpResponseRedirect(
        reverse_lazy("manager:team-update", kwargs={"pk": team.pk})
    )


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    template_name = "manager/team_form.html"
    form_class = TeamForm

    def get_success_url(self):
        return reverse_lazy("manager:team-detail", args=[self.object.pk])

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["segment"] = "team create"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.workers.add(self.request.user)
        return response

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if hasattr(user, "team") and user.team:
            return HttpResponseRedirect(
                reverse_lazy("manager:team-detail", args=[user.team.pk])
            )
        return super().get(request, *args, **kwargs)


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    template_name = "manager/team_form.html"
    form_class = TeamForm

    def get_success_url(self):
        return reverse_lazy("manager:team-detail", args=[self.object.pk])

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        team = context["team"]
        context["segment"] = f"team {team.pk} update"
        leader = team.leader
        context["workers"] = team.workers.all().exclude(pk=leader.pk)
        context["available_workers"] = Worker.objects.filter(team=None)
        return context


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = "manager/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "task delete"
        context["model"] = "task"
        return context


def toggle_project_by_team(
        request: HttpRequest,
        **kwargs) -> HttpResponseRedirect:
    user = request.user
    team = user.team
    project = get_object_or_404(Project, id=kwargs["pk"])
    if user == team.leader:
        if project.team:
            project.team = None
            project.save()
            for task in project.tasks.all():
                task.is_completed = False
                task.save()
                task.assigners.clear()
        else:
            project.team = team
            project.save()
    return HttpResponseRedirect(
        reverse_lazy(
            "manager:project-detail",
            kwargs={"pk": project.pk}
        )
    )
