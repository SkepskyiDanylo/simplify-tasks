from django.urls import path
from manager import views
from manager.views import delete_worker_from_team

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("accounts/login/", views.UserLoginView.as_view(), name="login"),
    path("accounts/logout/", views.UserLogoutView.as_view(), name="logout"),
    path("workers/", views.WorkerListView.as_view(), name="worker-list"),
    path("wokers/<int:pk>/", views.WorkerDetailView.as_view(), name="worker-detail"),
    path("profile/", views.ProfileDetailView.as_view(), name="current-profile"),
    path("workers/create/", views.WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/update/", views.WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", views.WorkerDeleteView.as_view(), name="worker-delete"),
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/toggle_assignment/", views.toggle_task_assignment, name="task-toggle-assignment"),
    path("tasks/<int:pk>/toggle_completed/", views.toggle_task_completed, name="task-toggle-completed"),
    path("task/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("task/<int:pk>/update/", views.TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task-delete"),
    path("task/create/", views.TaskCreateView.as_view(), name="task-create"),
    path("projects/", views.ProjectListView.as_view(), name="project-list"),
    path("project/<int:pk>/", views.ProjectDetailView.as_view(), name="project-detail"),
    path("project/team/<int:pk>/", views.toggle_project_by_team, name="project-team-toggle"),
    path("project/<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="project-delete"),
    path("project/<int:pk>/update/", views.ProjectUpdateView.as_view(), name="project-update"),
    path("project/create/", views.ProjectCreateView.as_view(), name="project-create"),
    path("teams/<int:pk>/", views.TeamDetailView.as_view(), name="team-detail"),
    path("add_worker/", views.add_worker_to_team, name="add-worker"),
    path("teams/create/", views.TeamCreateView.as_view(), name="team-create"),
    path("teams/<int:pk>/update/", views.TeamUpdateView.as_view(), name="team-update"),
    path("teams/<int:pk>/delete_worker/<int:user_pk>/", delete_worker_from_team, name="team-delete-worker"),
    path("teams/<int:pk>/delete/", views.TeamDeleteView.as_view(), name="team-delete"),
]

app_name = "manager"
