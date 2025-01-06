from django.urls import path
from manager import views

urlpatterns = [
    path("accounts/login/", views.UserLoginView.as_view(), name="login"),
    path("accounts/logout/", views.UserLogoutView.as_view(), name="logout"),
    path("workers/", views.WorkerListView.as_view(), name="worker-list"),
    path("woker/<int:pk>/", views.WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", views.WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/update/", views.WorkerUpdateView.as_view(), name="worker-update"),
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
]

app_name = "manager"
