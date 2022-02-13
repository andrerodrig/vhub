from django.urls import path
from . import views as v


# paths for /datasets
urlpatterns = [
    path("", v.DatasetsViewSet.as_view(
        {
            "get": "list",
            "post": "create",
        }
    )),
        path("<int:pk>", v.DatasetsDetailViewSet.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "delete",
        }
    ))
]

