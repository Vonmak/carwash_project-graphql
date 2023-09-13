from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True) 

    is_car_owner = models.BooleanField('car_owner', default=False)
    is_verified = models.BooleanField(default=False)
    
    otp = models.PositiveIntegerField(null=True, blank=True)
    otp_expiration = models.DateTimeField(null=True, blank=True)

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def is_otp_valid(self):
        """
        Check if the OTP is valid (not expired).
        """
        if self.otp and self.otp_expiration:
            return self.otp_expiration > timezone.now()
        return False

    def is_otp_match(self, entered_otp):
        """
        Check if the entered OTP matches the one in the database.
        """
        if self.is_otp_valid() and self.otp == entered_otp:
            return True
        return False

    def clear_otp(self):
        """
        Clear the OTP and OTP expiration time.
        """
        self.otp = None
        self.otp_expiration = None
        self.save()


# Car Owner Model
class CarOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='car_owner')

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def create_car_owner(sender, instance, created, **kwargs):
    """
    Signal handler to create a CarOwner instance when a User is created as a car owner.
    """
    if instance.is_car_owner and created and not instance.is_superuser and not instance.is_staff:
        CarOwner.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_car_owner(sender, instance, **kwargs):
    """
    Signal handler to save the CarOwner instance when the associated User is saved.
    """
    if instance.is_car_owner and not instance.is_superuser and not instance.is_staff:
        instance.car_owner.save()