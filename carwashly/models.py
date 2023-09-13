from django.db import models

class CarWash(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    services = models.ManyToManyField('CarWashService', related_name='carwashes', blank=True)
    premiums = models.ManyToManyField('PremiumMembership', related_name='carwashes', blank=True)

    def __str__(self):
        return self.name

class CarWashService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class PremiumMembership(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    period= models.CharField(max_length=15)
    benefits = models.ManyToManyField('PremiumBenefit')

    def __str__(self):
        return self.name

class PremiumBenefit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
