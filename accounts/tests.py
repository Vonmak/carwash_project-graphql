from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CarWashOwner, CarOwner

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        # Test creating a user with required fields
        user = User.objects.create_user(
            email='test@example.com',
            password='password123',
            first_name='John',
            last_name='Doe',
            is_carwash_owner= True,
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_carwash_owner)
        self.assertFalse(user.is_car_owner)

    def test_create_carwash_owner(self):
        # Test creating a car wash owner
        user = User.objects.create_user(
            email='wash@example.com',
            password='washpass123',
            first_name='Car',
            last_name='Wash',
            is_carwash_owner=True,
        )
        self.assertTrue(user.is_carwash_owner)
        self.assertFalse(user.is_car_owner)

    def test_create_car_owner(self):
        # Test creating a car owner
        user = User.objects.create_user(
            email='car@example.com',
            password='carpass123',
            first_name='Car',
            last_name='Owner',
            is_car_owner=True,
        )
        self.assertTrue(user.is_car_owner)
        self.assertFalse(user.is_carwash_owner)

class CarWashOwnerModelTest(TestCase):
    def test_create_carwash_owner_profile(self):
        user = User.objects.create_user(
            email='wash@example.com',
            password='washpass123',
            first_name='Car',
            last_name='Wash',
            is_carwash_owner=True,
        )
        carwash_owner = CarWashOwner.objects.get(user=user)
        self.assertEqual(carwash_owner.user, user)

class CarOwnerModelTest(TestCase):
    def test_create_car_owner_profile(self):
        user = User.objects.create_user(
            email='car@example.com',
            password='carpass123',
            first_name='Car',
            last_name='Owner',
            is_car_owner=True,
        )
        car_owner = CarOwner.objects.get(user=user)
        self.assertEqual(car_owner.user, user)
