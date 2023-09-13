from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CarWash, CarWashService, PremiumMembership, PremiumBenefit, CarWashOwner

User = get_user_model()

class CarWashModelTestCase(TestCase):
    def setUp(self):
        self.owner = User.objects.create(email='owner@test.com', is_carwash_owner=True)
        carwash_owner, created = CarWashOwner.objects.get_or_create(user=self.owner)
        self.carwash = CarWash.objects.create(owner=carwash_owner, name='Test Car Wash', description='A test car wash')

    def test_carwash_creation(self):
        carwash_owner = self.carwash.owner.user
        
        self.assertEqual(carwash_owner, self.owner)
        self.assertEqual(self.carwash.name, 'Test Car Wash')
        self.assertEqual(self.carwash.description, 'A test car wash')


    def test_carwash_services(self):
        service1 = CarWashService.objects.create(name='Service 1', description='Description 1')
        service2 = CarWashService.objects.create(name='Service 2', description='Description 2')
        self.carwash.services.add(service1)
        self.carwash.services.add(service2)

        self.assertIn(service1, self.carwash.services.all())
        self.assertIn(service2, self.carwash.services.all())

class PremiumMembershipModelTestCase(TestCase):
    def test_premium_membership_creation(self):
        membership = PremiumMembership.objects.create(name='Gold Membership', description='The best membership', price=19.99)
        self.assertEqual(membership.name, 'Gold Membership')
        self.assertEqual(membership.description, 'The best membership')
        self.assertEqual(membership.price, 19.99)

    def test_premium_membership_benefits(self):
        benefit1 = PremiumBenefit.objects.create(name='Benefit 1', description='Benefit Description 1')
        benefit2 = PremiumBenefit.objects.create(name='Benefit 2', description='Benefit Description 2')
        membership = PremiumMembership.objects.create(name='Silver Membership', description='A good membership', price=9.99)
        membership.benefits.add(benefit1)
        membership.benefits.add(benefit2)

        self.assertIn(benefit1, membership.benefits.all())
        self.assertIn(benefit2, membership.benefits.all())

class PremiumBenefitModelTestCase(TestCase):
    def test_premium_benefit_creation(self):
        benefit = PremiumBenefit.objects.create(name='Discount', description='Get 10% off')
        self.assertEqual(benefit.name, 'Discount')
        self.assertEqual(benefit.description, 'Get 10% off')

class CarWashOwnerModelTestCase(TestCase):
    def test_carwash_owner_creation(self):
        user = User.objects.create(email='owner@test.com', is_carwash_owner=True)
        carwash_owner, created = CarWashOwner.objects.get_or_create(user=user)
        self.assertEqual(carwash_owner.user, user)
