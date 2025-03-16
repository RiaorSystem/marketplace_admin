from django.contrib.auth.models import AbstractUser, Group, PermissionsMixin, BaseUserManager, Permission
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)  
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
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

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


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


