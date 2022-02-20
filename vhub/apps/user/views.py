from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.permissions import IsAdminUser
from vhub.apps.user.models import User
from vhub.apps.user.serializers import UserSerializer


class UserViewSet(viewsets.GenericViewSet):
    """
    Endpoint to handle User creation, listing, retrieving, updating and
    deletion.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Ony admin users can use thos viewset.
    permission_classes = [IsAdminUser]

    def list(self, request: Request):
        """Endpoint to list the users registered on the database."""
        serialized = self.serializer_class(
            self.get_queryset(),
            many=True,
            context={"request": request}
        )
        return Response(data=serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request: Request, pk: int):
        """Endpoint to retrieve the user detail info."""
        user_result = self.get_queryset().get(pk=pk)
        serialized = self.serializer_class(user_result)
        return Response(data=serialized.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk: int):
        """Endpoint to update the user data."""
        user_result = self.get_queryset().get(pk=pk)
        if user_result:
            serialized = self.serializer_class(user_result, data=request.data)
            if serialized.is_valid():
                serialized.save()
                return Response(
                    data=serialized.data, status=status.HTTP_201_CREATED
                )
            return Response(
                data=serialized.data, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, pk: int):
        """Endpoint to delete an user."""
        user_result = self.get_queryset().get(pk=pk)
        if user_result:
            user_result.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
