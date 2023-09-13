import pytest
from django.contrib.auth import get_user_model
from accounts.models import CarWashOwner, CarOwner

User = get_user_model()

@pytest.mark.django_db
def test_create_user():
    # Test creating a user with required fields
    user = User.objects.create_user(
        email='test@example.com',
        password='password123',
        first_name='John',
        last_name='Doe',
        is_carwash_owner=True,
    )
    assert user.email == 'test@example.com'
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.is_carwash_owner is True
    assert user.is_car_owner is False

@pytest.mark.django_db
def test_create_carwash_owner():
    # Test creating a car wash owner
    user = User.objects.create_user(
        email='wash@example.com',
        password='washpass123',
        first_name='Car',
        last_name='Wash',
        is_carwash_owner=True,
    )
    assert user.is_carwash_owner is True
    assert user.is_car_owner is False

@pytest.mark.django_db
def test_create_car_owner():
    # Test creating a car owner
    user = User.objects.create_user(
        email='car@example.com',
        password='carpass123',
        first_name='Car',
        last_name='Owner',
        is_car_owner=True,
    )
    assert user.is_car_owner is True
    assert user.is_carwash_owner is False

@pytest.mark.django_db
def test_create_carwash_owner_profile():
    user = User.objects.create_user(
        email='wash@example.com',
        password='washpass123',
        first_name='Car',
        last_name='Wash',
        is_carwash_owner=True,
    )
    carwash_owner = CarWashOwner.objects.get(user=user)
    assert carwash_owner.user == user

@pytest.mark.django_db
def test_create_car_owner_profile():
    user = User.objects.create_user(
        email='car@example.com',
        password='carpass123',
        first_name='Car',
        last_name='Owner',
        is_car_owner=True,
    )
    car_owner = CarOwner.objects.get(user=user)
    assert car_owner.user == user
