from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(Group, related_name="customuser_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions")

    USERNAME_FIELD = 'email'  # Use email for authentication
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

User = get_user_model()
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    bio = models.TextField(max_length = 100,blank = True)
    profile_picture = models.ImageField(upload_to ='profile-pictures/',blank=True,null=True)
    phone_number = models.CharField(max_length=15,blank=True)
    address = models.CharField(max_length=255,blank = True)

def __str__(self):
    return f'{self.user.email}Profile'

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
     Profile.objects.create(user=instance)
@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()


