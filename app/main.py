from fastapi import FastAPI
from .routers import job, aiml
from .config import settings
from fastapi.openapi.utils import get_openapi

app = FastAPI()

app.include_router(job.router)
app.include_router(aiml.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my playground"}


@app.get("/health")
def health_check():
    return {f"{settings.ENV} OK"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My Playground for Python, Deep learning and more",
        version="1.0",
        summary="This is a my playground",
        description="Prototype of test microservices, Traffic Sign classification",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
