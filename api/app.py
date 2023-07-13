from fastapi import FastAPI

from .routers import security, books

app = FastAPI(
    title="Library"
)

app.include_router(security.router)
app.include_router(
    books.router,
    tags=["books"])


@app.get("/")
async def read_root():
    return {"Hello": "hi"}
