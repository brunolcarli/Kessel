import graphene
import discord_game.schema as backend_schema


queries = (
    graphene.ObjectType,
    backend_schema.Query,
)

# mutations = (
#     graphene.ObjectType,
#     backend_schema.Mutation
# )

class Query(*queries):
    pass


# class Mutation(*mutations):
#     pass


# schema = graphene.Schema(query=Query, mutation=Mutation)
schema = graphene.Schema(query=Query)
