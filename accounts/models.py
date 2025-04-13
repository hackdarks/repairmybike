from django.db import models
from django.contrib.auth.models import AbstractUser

class SupabaseUser(AbstractUser):
    email = models.EmailField(unique=True)
    supabase_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Remove null=True because it's unnecessary for ManyToManyField
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='supabase_user_set'  # Custom related_name (optional)
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='supabase_user_permissions_set'  # Custom related_name (optional)
    )

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    address = models.TextField()
    profile_photo = models.ImageField(upload_to="profiles/")
    vehicle_name = models.CharField(max_length=255)
    vehicle_type = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)

    def __str__(self):
        return self.email