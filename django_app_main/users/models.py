from django.contrib.auth.models import AbstractUser, Group, PermissionsMixin, BaseUserManager, Permission
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None,**extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)

        if username is None:
            username = email.split("@")[0]
        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, username, **extra_fields)
    
class UserRoles(models.TextChoices):
    ADMIN = "admin", "Admin"
    SELLER = "seller", "Seller"
    BUYER = "buyer", "Buyer"

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    bio =  models.TextField(blank=True, null=True)
    role = models.CharField(max_length=10, choices = UserRoles.choices, default=UserRoles.BUYER)

    groups = models.ManyToManyField(Group, related_name="customuser_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions")
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Contact(models.Model):
    """Stores the contacts a user has saved"""
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="contacts")
    contact_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="added_by", null=True, blank=True)
    phone_number = models.CharField(max_length=15)

    class Meta:
        unique_together = ("owner", "phone_number")

    def save(self, *args, **kwargs):
        """Linking to a registered user if the phone number matches"""
        if not self.contact_user:
            self.contact_user = CustomUser.objects.filter(phone_number=self.phone_number).first()
        super().save(*args, **kwargs)


