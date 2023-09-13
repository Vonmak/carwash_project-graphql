import graphene
from accounts.schema import AuthMutations, AuthQuery
from carwashly.schema import CarWashMutation, CarWashQuery
from carly.schema import CarsMutation, CarsQuery



class Query(graphene.ObjectType):
    auth_queries= AuthQuery()
    carwash_queries = CarWashQuery()
    cars_queries = CarsQuery()

class Mutation(graphene.ObjectType):
    auth_mutations = AuthMutations()
    carwash_mutations = CarWashMutation()
    cars_mutations = CarsMutation



schema = graphene.Schema(query=Query, mutation=Mutation)