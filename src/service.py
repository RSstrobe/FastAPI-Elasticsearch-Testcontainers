from repository import ElasticRepository
from schemas import MoviesSchema


class SearchService:
    def __init__(self, repo: ElasticRepository):
        self.repo = repo

    async def search(self, search_query: str) -> list[MoviesSchema]:
        body = {
            "query": {
                "multi_match": {
                    "query": search_query,
                    "fields": [
                        "title",
                        "description",
                        "genres"
                    ],
                }
            },
            "aggs": {
                "unique_ids": {
                    "terms": {
                        "field": "id.keyword",
                        "size": 1
                    }
                }
            }
        }
        result_es = await self.repo.search(body)

        response = [MoviesSchema(**doc["_source"]) for doc in result_es["hits"]["hits"]]

        return response
