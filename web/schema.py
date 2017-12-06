import graphene

from nodes_app import schema as nodes_schema


class Query(nodes_schema.Query, graphene.ObjectType):
    pass


class Mutations(graphene.ObjectType):
    create_node = nodes_schema.CreateNode.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
