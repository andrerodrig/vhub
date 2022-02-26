from django.urls import path
from . import views as v


# paths for /data
urlpatterns = [
    path("datasets/<int:dataset_id>", v.DataViewSet.as_view(
        {
            "get": "list",
            "post": "create",
        }
    )),
    path("<int:pk>", v.DataDetailViewSet.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "delete",
        }
    ))
]
