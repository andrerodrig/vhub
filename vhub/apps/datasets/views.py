import io

from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Datasets
from vhub.apps.data.models import Data
from vhub.lib.data import Data as LibData
from .serializers import DatasetsSerializer, DatasetsDetailSerializer
from .permissions import IsOwnerOrReadOnly


class DatasetsViewSet(viewsets.GenericViewSet):
    """Viewset for dataset listing and creation."""
    queryset = Datasets.objects.all()
    serializer_class = DatasetsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser]

    def list(self, request: Request) -> Response:
        """Endpoint to handling the datasets listing."""
        dataset_list = self.get_queryset().filter(owner=request.user.id)
        page = self.paginate_queryset(dataset_list)
        if page is not None:
            serialized = self.get_serializer(page, many=True)
            return self.get_paginated_response(serialized.data)
        serialized = self.serializer_class(
            dataset_list,
            many=True,
            context={"request": request}
        )
        return Response(data=serialized.data)

    @swagger_auto_schema(
        operation_id='Upload file',
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="Document"
            )
        ],
    )
    def create(self, request: Request) -> Response:
        """Endpoint to handling dataset creation."""
        serialized = self.serializer_class(
            data=request.data,
            context={"request": request}
        )
        if serialized.is_valid():
            self.perform_create(serializer=serialized)
            # read the value from the file to the buffer
            file_in_buffer = request.data.get("file").file
            str_buf_file = io.StringIO(
                file_in_buffer.getvalue().decode("utf-8")
            )
            # Calling the method from the lib to insert the data
            # from the dataset in the table Data.
            LibData.save_csv_data(
                str_buf_file,
                Data.objects.create,
                dataset_id=serialized.data.get("id"),
                hostname="ASSET - HOSTNAME",
                ip_address="ASSET - IP_ADDRESS",
                title="VULNERABILITY - TITLE",
                severity="VULNERABILITY - SEVERITY",
                cvss="VULNERABILITY - CVSS",
                publication_date="VULNERABILITY - PUBLICATION_DATE",
            )
            return Response(
                data=serialized.data, status=status.HTTP_201_CREATED
            )
        return Response(
            data=serialized.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user, file=self.request.FILES.get("file")
        )


class DatasetsDetailViewSet(viewsets.GenericViewSet):
    """Endpoint to handle data , retrieving and deletion."""
    queryset = Datasets.objects.all()
    serializer_class = DatasetsDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def retrieve(self, request: Request, pk: int) -> Response:
        """Endpoint to get the informations about a dataset based on its id."""
        dataset = self.get_queryset().filter(owner=request.user.id)
        if dataset:
            dataset = dataset.get(pk=pk)
            serialized = self.serializer_class(
                dataset,
                context={"request": request}
            )
            return Response(data=serialized.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request: Request, pk: int) -> Response:
        """Endpoint to update a dataset."""
        dataset = self.get_queryset().filter(
            owner_id=request.user.id
        ).get(pk=pk)
        serialized = self.serializer_class(
            instance=dataset,
            data=request.data,
            context={"request": request}
        )
        if serialized.is_valid():
            serialized.save()
            return Response(
                data=serialized.data, status=status.HTTP_202_ACCEPTED
            )
        return Response(
            data=serialized.errors, status=status.HTTP_404_NOT_FOUND
        )

    def partial_update(self, request: Request, pk: int) -> Response:
        """Endpoint to partial updating of a dataset."""
        dataset = self.get_queryset().filter(
            owner_id=request.user.id
        ).get(pk=pk)
        serialized = self.serializer_class(
            instance=dataset,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        if serialized.is_valid():
            serialized.save()
            return Response(
                data=serialized.data, status=status.HTTP_202_ACCEPTED
            )
        return Response(
            data=serialized.errors, status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request: Request, pk: int) -> Response:
        "Endpoint to delete a dataset."
        dataset = self.get_queryset().filter(
            owner_id=request.user.id
        ).get(pk=pk)
        if dataset:
            dataset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
