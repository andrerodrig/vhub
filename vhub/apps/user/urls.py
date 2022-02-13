from rest_framework.urls import path
from . import views as v


# paths for /user
urlpatterns = [
    path("", v.UserViewSet.as_view({"get": "list"}), name="list"),
    path("<int:pk>", v.UserViewSet.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "delete": "delete",
        }
    ), name="detail")
]