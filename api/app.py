from fastapi import FastAPI

from .routers import security, books
from .graphql.app import graphql_app

app = FastAPI(
    title="Library"
)

app.include_router(security.router)
app.include_router(
    books.router,
    tags=["books"])
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


@app.get("/")
async def read_root():
    return {"Hello": "hi"}
