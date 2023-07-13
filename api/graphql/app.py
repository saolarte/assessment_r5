
import strawberry
from strawberry.asgi import GraphQL

from .queries import Query


schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)