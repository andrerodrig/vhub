from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Creates a custom user model manager."""
    
    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **extra_fields
    ):
        """Creates a user with the fields passed above."""
        if not email:
            raise ValueError(_("The Email field cannot be empty."))
        if not first_name:
            raise ValueError(_("The First Name field cannot be empty."))
        if not last_name:
            raise ValueError(_("The Last Name field cannot be empty."))
        if not password:
            raise ValueError(_("The Password field cannot be empty."))
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(
        self,
        email,
        first_name: str,
        last_name: str,
        password: str,
        **extra_fields
    ):
        """Creates a Superuser with the fields passed above."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("A superuser should be an staff user."))
        if extra_fields.get("is_active") is not True:
            raise ValueError(_("A superuser should be an active user."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("A superuser must have the is_superuser field setted as True."))
        return self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields
        )
        
    
            