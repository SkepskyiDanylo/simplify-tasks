from django.urls import path
from manager import views

urlpatterns = [
    path("accounts/login/", views.UserLoginView.as_view(), name="login"),
    path("accounts/logout/", views.UserLogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", views.WorkerDetailView.as_view(), name="profile"),
]

app_name = "manager"
