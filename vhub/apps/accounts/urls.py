from rest_framework.urls import path
from . import views as v


urlpatterns = [
    path("register", v.RegisterViewSet.as_view({"post": "register"}), name="register"),
    path("login", v.LoginViewSet.as_view({"post": "login"}), name="login"),
]