import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from httpx import AsyncClient
from testcontainers.elasticsearch import ElasticSearchContainer

from deps import get_elasctic_repo
from init_elastic import setup_elastic
from main import app
from repository import ElasticRepository


@pytest.fixture(name="elastic_container", scope="session")
def elastic_container():
    container = ElasticSearchContainer("elasticsearch:8.6.2")
    container.start()
    yield container
    container.stop()


@pytest.fixture(name="elastic_client", scope="session")
def elastic_client(elastic_container):
    client = AsyncElasticsearch(elastic_container.get_url())
    yield client
    client.close()


@pytest_asyncio.fixture(name="setup_elastic", autouse=True)
async def setup_db(elastic_client):
    await setup_elastic(elastic_client)


@pytest.fixture(name="test_client", scope="session")
def test_client(elastic_client):
    def test_get_elastic_repo():
        return ElasticRepository(client=elastic_client)

    app.dependency_overrides[get_elasctic_repo] = test_get_elastic_repo

    return AsyncClient(app=app, base_url="http://test")
