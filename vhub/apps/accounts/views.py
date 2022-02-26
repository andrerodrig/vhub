from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from vhub.apps.accounts.serializers import LoginSerializer, RegisterSerializer
from vhub.apps.user.serializers import UserSerializer


class RegisterViewSet(viewsets.GenericViewSet):
    """Handles the user registering."""
    serializer_class = RegisterSerializer
    permission_classes = []

    def register(self, request: Request):
        serialized = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        if serialized.is_valid():
            user = serialized.save()
            token = Token.objects.create(user=user)
            return Response(
                data={
                    "data": UserSerializer(user).data,
                    "token": token.key
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            data=serialized.errors, status=status.HTTP_400_BAD_REQUEST
        )


class LoginViewSet(viewsets.GenericViewSet):
    """Handles the user login."""
    serializer_class = LoginSerializer
    permission_classes = []

    def login(self, request: Request):
        serialized = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        if serialized.is_valid():
            user = serialized.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "data": UserSerializer(user).data,
                    "token": token.key
                },
                status=status.HTTP_200_OK
            )
