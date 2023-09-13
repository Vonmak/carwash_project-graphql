from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Car
from accounts.models import CarOwner
# Create your tests here.

User =get_user_model()

class CarModelTestCase(TestCase):
    def setUp(self):
        self.owner = User.objects.create(email='owner@test.com', is_car_owner=True)
        car_owner, created = CarOwner.objects.get_or_create(user=self.owner)
        self.car = Car.objects.create(owner=car_owner, make='Toyota',model='Extrail',license_plate='kcs124a', description='A test car')

    def test_car_creation(self):
        car_owner = self.car.owner.user
        
        self.assertEqual(car_owner, self.owner)
        self.assertEqual(self.car.license_plate, 'kcs124a')
        self.assertEqual(self.car.description, 'A test car')