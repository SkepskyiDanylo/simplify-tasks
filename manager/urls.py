from django.urls import path
from manager import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("accounts/login/", views.UserLoginView.as_view(), name="login"),
    path("accounts/logout/", views.UserLogoutView.as_view(), name="logout"),
    path("workers/", views.WorkerListView.as_view(), name="worker-list"),
    path("woker/<int:pk>/", views.WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", views.WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/update/", views.WorkerUpdateView.as_view(), name="worker-update"),
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/toggle_assignment/", views.toggle_task_assignment, name="task-toggle-assignment"),
    path("tasks/<int:pk>/toggle_completed/", views.toggle_task_completed, name="task-toggle-completed"),
    path("task/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("task/<int:pk>/update/", views.TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task-delete"),
    path("task/create/", views.TaskCreateView.as_view(), name="task-create"),
    path("projects/", views.ProjectListView.as_view(), name="project-list"),
]

app_name = "manager"
