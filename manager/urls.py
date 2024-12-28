from django.urls import path
from manager import views

urlpatterns = [
    path("accounts/login/", views.UserLoginView.as_view(), name="login"),
]

app_name = "manager"
