from contextlib import asynccontextmanager

from fastapi import FastAPI

import deps
from api import api_router
from init_elastic import setup_elastic


@asynccontextmanager
async def lifespan(_: FastAPI):
    deps.elastic = deps.get_elastic_client()
    await setup_elastic(deps.elastic)
    yield
    await deps.elastic.close()


def create_app() -> FastAPI:
    app = FastAPI(
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )
    app.include_router(api_router)
    return app
