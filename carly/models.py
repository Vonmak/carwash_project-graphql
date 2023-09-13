from django.db import models
from accounts.models import CarOwner
from django.core.validators import RegexValidator

# Create your models here.
class Car(models.Model):
    alphanumeric_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9]*$',
        message='License plate can only contain alphanumeric characters.',
    )


    owner =models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name='cars')
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    description = models.TextField()
    license_plate = models.CharField(max_length=15, unique=True, validators=[alphanumeric_validator])


    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate}) {self.owner.user.email}"
