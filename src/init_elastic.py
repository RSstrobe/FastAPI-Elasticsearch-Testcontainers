import json
import uuid
from typing import Iterator

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk


class SetupElastic:
    index_name = "movies"
    es_file_name = "data"

    def __init__(self, client: AsyncElasticsearch):
        self.client = client

    @staticmethod
    def load_json_data(name: str) -> any:
        with open(f"../data/{name}.json", "r") as fp:
            data = json.load(fp)
        return data

    async def gen_data(self, data: dict) -> Iterator[dict[str, str]]:
        for row in data:
            id = uuid.uuid4()
            yield {
                "_index": self.index_name,
                "_id": str(id),
                "_source": {
                    "id": str(id),
                    "imdb_rating": row["imdb_rating"],
                    "genres": row["genres"],
                    "title": row["title"],
                    "description": row["description"],
                }
            }

    async def insert_data(self):
        data = self.load_json_data(self.es_file_name)

        await async_bulk(
            client=self.client,
            actions=self.gen_data(data)
        )

    async def setup_elastic(self):
        is_index_exists = await self.client.indices.exists(index=self.index_name)
        if not is_index_exists:
            index_mapping = self.load_json_data(self.index_name)
            await self.client.indices.create(index=self.index_name, body=index_mapping)
            await self.insert_data()


async def setup_elastic(client: AsyncElasticsearch) -> None:
    await SetupElastic(client).setup_elastic()
