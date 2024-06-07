from elasticsearch import AsyncElasticsearch


class ElasticRepository:
    index = "movies"

    def __init__(self, client: AsyncElasticsearch):
        self.client = client

    async def search(self, body: dict[str, dict]):
        return await self.client.search(index=self.index, body=body)
