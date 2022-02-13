from django.shortcuts import render
from rest_framework import serializers
from django.contrib.auth import authenticate

from vhub.apps.user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Password"}
    )
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get("password"))
        user.save()
        return user
    
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "password"]

        write_only_fields = ["password"]
        
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Password"})
    
    def validate(self, data):
        user = authenticate(**data)
        if user:
            if user.is_active:
                return user
            else:
                raise serializers.ValidationError(
                    "This account has been disabled."
                )
        raise serializers.ValidationError(
            "Incorrect credentials."
        )
    
    class Meta:
        model = User
        fields = ["email", "password"]
        