from typing import Annotated

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from starlette.requests import Request

from config import settings
from repository import ElasticRepository
from service import SearchService

elastic: AsyncElasticsearch | None = None


def get_elastic_client() -> AsyncElasticsearch:
    return AsyncElasticsearch(settings.elastic_url)


def get_elasctic_repo(_: Request):
    return ElasticRepository(client=elastic)


ElasticRepo = Annotated[ElasticRepository, Depends(get_elasctic_repo)]


def get_search_service(repo: ElasticRepo):
    return SearchService(repo)


Service = Annotated[SearchService, Depends(get_search_service)]
