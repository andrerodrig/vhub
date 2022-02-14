from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from .models import Data
from .serializers import DataSerializer, DataDetailSerializer
from .permissions import IsOwnerOrReadOnly


class DataViewSet(viewsets.GenericViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def list(self, request: Request, dataset_id: int) -> Response:
        """Endpoint to handling data listing."""
        data_list = self.get_queryset().filter(dataset_id=dataset_id)
        page = self.paginate_queryset(data_list)
        if page is not None:
            serialized = self.get_serializer(page, many=True)
            return self.get_paginated_response(serialized.data)
        serialized = self.serializer_class(data_list, many=True, context={"request": request})
        return Response(data=serialized.data)

    def create(self, request: Request) -> Response:
        """ Endpoint to handling data creation."""
        serialized = self.serializer_class(data=request.data, context={"request": request})
        if serialized.is_valid():
            self.perform_create(serializer=serialized)
            return Response(
                data=serialized.data, status=status.HTTP_201_CREATED
            )
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(dataset__owner_id=self.request.user)


class DataDetailViewSet(viewsets.GenericViewSet):
    """Endpoint to handle data , retrieving and deletion."""
    queryset = Data.objects.all()
    serializer_class = DataDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def retrieve(self, request: Request, pk: int) -> Response:
        data = self.get_queryset().filter(dataset__owner_id=request.user.id).get(pk=pk)
        if data:
            serialized = self.serializer_class(data, context={"request": request})
            return Response(data=serialized.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_404_NOT_FOUND)

    def update(self, request: Request, pk: int) -> Response:
        """Endpoint to update a row from the dataset saved on the database."""
        data = self.get_queryset().filter(dataset__owner_id=request.user.id).get(pk=pk)
        serialized = self.serializer_class(
            instance=data,
            data=request.data,
            context={"request": request}
        )
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serialized.errors, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request: Request, pk: int) -> Response:
        """Endpoint to update a row from the dataset saved on the database."""
        data = self.get_queryset().filter(dataset__owner_id=request.user.id).get(pk=pk)
        serialized = self.serializer_class(
            instance=data,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serialized.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, pk: int) -> Response:
        """Endpoint to delete a data from the dataset saved in the database."""
        data = self.get_queryset().filter(dataset__owner_id=request.user.id).get(pk=pk)
        if data:
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)