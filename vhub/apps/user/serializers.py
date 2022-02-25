from rest_framework import serializers

from vhub.apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]