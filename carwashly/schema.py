import graphene
from graphene_django.types import DjangoObjectType
from .models import CarWash, CarWashService, PremiumBenefit, PremiumMembership

# Define a GraphQL type for CarWash
class CarWashType(DjangoObjectType):
    class Meta:
        model = CarWash

# Define a GraphQL type for CarWashService
class CarWashServiceType(DjangoObjectType):
    class Meta:
        model = CarWashService
    
# Define a GraphQl type for PremiumMembership
class PremiumMembershipType(DjangoObjectType):
    class Meta:
        model = PremiumMembership

# Define a graphqltype for premiumbenefit
class PremiumBenefitType(DjangoObjectType):
    class Meta:
        model = PremiumBenefit

# Create a mutation to create a new CarWash
class CreateCarWash(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()

    carwash = graphene.Field(CarWashType)

    def mutate(self, info, name, description):
        carwash = CarWash(name=name, description=description)
        carwash.save()
        return CreateCarWash(carwash=carwash)

# Create a mutation to create a new CarWashService
class CreateCarWashService(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()

    carwashservice = graphene.Field(CarWashServiceType)

    def mutate(self, info, name, description):
        carwashservice = CarWashService(name=name, description=description)
        carwashservice.save()
        return CreateCarWashService(carwashservice=carwashservice)

# Create a mutation to update an existing CarWash
class UpdateCarWash(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        description = graphene.String()
        service_id = graphene.Int()

    carwash = graphene.Field(CarWashType)
    service = graphene.Field(CarWashServiceType)

    def mutate(self, info, id, name=None, description=None, service_id=None):
        try:
            carwash = CarWash.objects.get(pk=id)
            if name is not None:
                carwash.name = name
            if description is not None:
                carwash.description = description
            if service_id is not None:
                try:
                    service = CarWashService.objects.get(pk=service_id)
                    carwash.services.add(service)
                    return UpdateCarWash(carwash=carwash, service=service)
                except CarWashService.DoesNotExist:
                    return UpdateCarWash(carwash=carwash, service=None)
            
            carwash.save()
            return UpdateCarWash(carwash=carwash)
        except CarWash.DoesNotExist:
            return UpdateCarWash(carwash=None, service=None)


# Create a mutation to delete a CarWash
class DeleteCarWash(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            carwash = CarWash.objects.get(pk=id)
            carwash.delete()
            success = True
        except CarWash.DoesNotExist:
            success = False
        return DeleteCarWash(success=success)

# Create a mutation to update an existing CarWashService
class UpdateCarWashService(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        description = graphene.String()
        service_id = graphene.Int()

    carwashservice = graphene.Field(CarWashServiceType)
    

    def mutate(self, info, id, name, description):
        carwashservice = CarWashService.objects.get(pk=id)
        if name:
            carwashservice.name = name
        if description:
            carwashservice.description = description
        carwashservice.save()
        return UpdateCarWashService(carwashservice=carwashservice)

# Create a mutation to delete a CarWashService
class DeleteCarWashService(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            carwashservice = CarWashService.objects.get(pk=id)
            carwashservice.delete()
            success = True
        except CarWashService.DoesNotExist:
            success = False
        return DeleteCarWashService(success=success)


class CreatePremiumMembership(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()
        price = graphene.Decimal()
        period = graphene.String()

    premiummembership = graphene.Field(PremiumMembershipType)

    def mutate(self, info, name, description, price, period):
        premiummembership = PremiumMembership(name=name, description=description, price=price, period=period)
        premiummembership.save()
        return CreatePremiumMembership(premiummembership=premiummembership)

class CreatePremiumBenefit(graphene.Mutation):
    class Arguments:
        name=graphene.String()
        description=graphene.String()

    premiumbenefit = graphene.Field(PremiumBenefitType)

    def mutate(self, info, name, description):
        premiumbenefit = PremiumBenefit(name= name, description=description)
        premiumbenefit.save()
        return CreatePremiumBenefit(premiumbenefit=premiumbenefit)


class UpdatePremiumMembership(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        description = graphene.String()
        price = graphene.Decimal()
        period = graphene.String()
        benefit_id = graphene.Int()

    premiummembership = graphene.Field(PremiumMembershipType)
    benefit = graphene.Field(PremiumBenefitType)

    def mutate(self, info, id, name=None, description=None, price=None, period=None, benefit_id=None):
        try:
            premiummembership = PremiumMembership.objects.get(pk=id)

            if name is not None:
                premiummembership.name = name
            if description is not None:
                premiummembership.description = description
            if price is not None:
                premiummembership.price = price
            if period is not None:
                premiummembership.period = period

            if benefit_id is not None:
                try:
                    benefit = PremiumBenefit.objects.get(pk=benefit_id)
                    premiummembership.benefits.add(benefit)
                    return UpdatePremiumMembership(premiummembership=premiummembership, benefit=benefit)
                except PremiumBenefit.DoesNotExist:
                    raise Exception("PremiumBenefit with ID {} does not exist.".format(benefit_id))

            premiummembership.save()
            return UpdatePremiumMembership(premiummembership=premiummembership)
        except PremiumMembership.DoesNotExist:
            raise Exception("PremiumMembership with ID {} does not exist.".format(id))

class UpdatePremiumBenefit(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        description = graphene.String()

    benefit = graphene.Field(PremiumBenefitType)

    def mutate(self, info, id, name=None, description=None):
        try:
            premiumbenefit = PremiumBenefit.objects.get(pk=id)

            if name is not None:
                premiumbenefit.name = name
            if description is not None:
                premiumbenefit.description = description

            premiumbenefit.save()
            return UpdatePremiumBenefit(premiumbenefit=premiumbenefit)
        except PremiumBenefit.DoesNotExist:
            raise Exception("PremiumBenefit with ID {} does not exist.".format(id))

# Create a mutation to delete a PremiumMembership
class DeletePremiumMembership(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            premiummembership = PremiumMembership.objects.get(pk=id)
            premiummembership.delete()
            success = True
        except PremiumMembership.DoesNotExist:
            raise Exception("PremiumMembership with ID {} does not exist.".format(id))
            success = False
        return DeletePremiumMembership(success=success)

# Create a mutation to delete a PremiumMembership
class DeletePremiumBenefit(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            premiumbenefit = PremiumBenefit.objects.get(pk=id)
            premiumbenefit.delete()
            success = True
        except PremiumBenefit.DoesNotExist:
            raise Exception("PremiumBenefit with ID {} does not exist.".format(id))
            success = False
        return DeletePremiumBenefit(success=success)

class RemoveServiceFromCarwash(graphene.Mutation):
    class Arguments:
        carwash_id = graphene.Int()
        service_id = graphene.Int()

    carwash = graphene.Field(CarWashType)
    service = graphene.Field(CarWashServiceType)

    def mutate(self, info, carwash_id, service_id):
        try:
            carwash = CarWash.objects.get(pk=carwash_id)
            service = CarWashService.objects.get(pk=service_id)
            
            if service in carwash.services.all():
                carwash.services.remove(service)
                return RemoveServiceFromCarWash(carwash=carwash, service=service)
            else:
                raise Exception("Service with ID {} is not associated with Carwash with ID {}.".format(service_id, carwash_id))

        except CarWash.DoesNotExist:
            raise Exception("Carwash with ID {} does not exist.".format(carwash_id))

        except CarWashService.DoesNotExist:
            raise Exception("Service with ID {} does not exist.".format(service_id))
        
class RemovePremiumFromCarwash(graphene.Mutation):
    class Arguments:
        carwash_id = graphene.Int()
        premium_id = graphene.Int()

    carwash = graphene.Field(CarWashType)
    premium = graphene.Field(PremiumMembershipType)

    def mutate(self, info, carwash_id, premium_id):
        try:
            carwash = CarWash.objects.get(pk=carwash_id)
            premium = PremiumMembership.objects.get(pk=premium_id)
            
            if premium in carwash.premiums.all():
                carwash.premiums.remove(benefit)
                return RemovePremiumFromCarwash(carwash=carwash, premium=premium)
            else:
                raise Exception("Premium with ID {} is not associated with CarWash with ID {}.".format(premium_id, carwash_id))

        except CarWash.DoesNotExist:
            raise Exception("Carwash with ID {} does not exist.".format(carwash_id))

        except PremiumMembership.DoesNotExist:
            raise Exception("Premium with ID {} does not exist.".format(premium_id))

class RemoveBenefitFromPremiumMembership(graphene.Mutation):
    class Arguments:
        premium_membership_id = graphene.Int()
        benefit_id = graphene.Int()

    premium_membership = graphene.Field(PremiumMembershipType)
    benefit = graphene.Field(PremiumBenefitType)

    def mutate(self, info, premium_membership_id, benefit_id):
        try:
            premium_membership = PremiumMembership.objects.get(pk=premium_membership_id)
            benefit = PremiumBenefit.objects.get(pk=benefit_id)
            
            if benefit in premium_membership.benefits.all():
                premium_membership.benefits.remove(benefit)
                return RemoveBenefitFromPremiumMembership(premium_membership=premium_membership, benefit=benefit)
            else:
                raise Exception("Benefit with ID {} is not associated with PremiumMembership with ID {}.".format(benefit_id, premium_membership_id))

        except PremiumMembership.DoesNotExist:
            raise Exception("PremiumMembership with ID {} does not exist.".format(premium_membership_id))

        except PremiumBenefit.DoesNotExist:
            raise Exception("Benefit with ID {} does not exist.".format(benefit_id))


# Define a GraphQL query for retrieving CarWash objects
class CarWashQuery(graphene.ObjectType):
    carwashes = graphene.List(CarWashType)

    def resolve_carwashes(self, info):
        return CarWash.objects.all()

    # Define a GraphQL query for retrieving CarWashService objects
    carwash_services = graphene.List(CarWashServiceType)

    def resolve_carwash_services(self, info):
        return CarWashService.objects.all()

    # Define a GraphQL query for retrieving PremiumMembership objects
    premium_memberships = graphene.List(PremiumMembershipType)

    def resolve_premium_memberships(self, info):
        return PremiumMembership.objects.all()

    # Define a GraphQL query for retrieving PremiumBenefit objects
    premium_benefits = graphene.List(PremiumBenefitType)

    def resolve_premium_benefits(self, info):
        return PremiumBenefit.objects.all()


# Create a GraphQL schema with the mutations
class CarWashMutation(graphene.ObjectType):
    create_carwash = CreateCarWash.Field()
    create_carwashservice = CreateCarWashService.Field()
    create_premiummembership= CreatePremiumMembership.Field()
    create_premiumbenefit = CreatePremiumBenefit.Field()
    update_carwash = UpdateCarWash.Field()
    update_carwashservice = UpdateCarWashService.Field()
    update_premiummembership= UpdatePremiumMembership.Field()
    update_premiumbenefit=UpdatePremiumBenefit.Field()
    delete_carwash = DeleteCarWash.Field()
    delete_carwashservice = DeleteCarWashService.Field()
    delete_premiummembership= DeletePremiumMembership.Field()
    delete_premiumbenefit = DeletePremiumBenefit.Field()
    remove_service_from_carwash=RemoveServiceFromCarwash.Field()
    remove_premium_from_carwash=RemovePremiumFromCarwash.Field()
    remove_benefit_from_premiummembership=RemoveBenefitFromPremiumMembership.Field()


# Create a GraphQL schema with queries and mutations
# schema = graphene.Schema(query=Query, mutation=Mutation)
 