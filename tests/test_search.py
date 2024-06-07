import pytest


@pytest.mark.parametrize(
    "data, expected_answer",
    [
        (
                {
                    "search_query": "Fight"
                },
                {
                    "data": {
                        'imdb_rating': 8.8,
                        'genres': ['Drama'],
                        'title': 'Fight Club',
                        'description': 'An insomniac office worker and a devil-may-care soapmaker form an'
                                       ' underground fight club that evolves into something much, much more.'
                    },
                    "status": 200,
                }
        ),
    ],
)
@pytest.mark.asyncio
async def test_search(test_client, data, expected_answer):
    response = await test_client.get("/search", params=data)
    assert response.status_code == expected_answer["status"]
    assert response.json()[0] == expected_answer["data"]
