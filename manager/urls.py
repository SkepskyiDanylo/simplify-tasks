from django.urls import path
from manager import views

urlpatterns = [
    path("accounts/login/", views.UserLoginView.as_view(), name="login"),
    path("accounts/logout/", views.UserLogoutView.as_view(), name="logout"),
]

app_name = "manager"
