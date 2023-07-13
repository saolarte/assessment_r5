
import strawberry
from strawberry.asgi import GraphQL

from .queries import Query
from .mutations import Mutation


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)