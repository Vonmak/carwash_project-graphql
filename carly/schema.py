import graphene
from graphene import InputObjectType
from graphene_django.types import DjangoObjectType
from .models import Car
from accounts.models import CarOwner

# Define a GraphQL type for the Car model
class CarType(DjangoObjectType):
    class Meta:
        model = Car

# Define an InputObjectType for creating or updating a car
class CarInput(InputObjectType):
    make = graphene.String(required=True)
    model = graphene.String(required=True)
    description = graphene.String()
    license_plate = graphene.String(required=True)
    owner_id = graphene.Int(required=True)

# Define a mutation to create a new car
class CreateCar(graphene.Mutation):
    class Arguments:
        input = CarInput(required=True)

    car = graphene.Field(CarType)

    @staticmethod
    def mutate(root, info, input):
        owner_id = input.pop("owner_id")
        owner = CarOwner.objects.get(pk=owner_id)
        car = Car(**input, owner=owner)
        car.save()
        return CreateCar(car=car)

# Define a mutation to update an existing car
class UpdateCar(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = CarInput(required=True)

    car = graphene.Field(CarType)

    @staticmethod
    def mutate(root, info, id, input):
        car = Car.objects.get(pk=id)
        for attr, value in input.items():
            setattr(car, attr, value)
        car.save()
        return UpdateCar(car=car)

# Define a mutation to delete a car
class DeleteCar(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        car = Car.objects.get(pk=id)
        car.delete()
        return DeleteCar(success=True)

# Define a query to fetch all cars
class CarsQuery(graphene.ObjectType):
    all_cars = graphene.List(CarType)

    def resolve_all_cars(self, info):
        return Car.objects.all()

# Define the root mutation
class CarsMutation(graphene.ObjectType):
    create_car = CreateCar.Field()
    update_car = UpdateCar.Field()
    delete_car = DeleteCar.Field()


# Define the root schema
# schema = graphene.Schema(query=Query, mutation=Mutation)