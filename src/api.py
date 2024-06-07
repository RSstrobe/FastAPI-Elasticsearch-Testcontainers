from fastapi import APIRouter, status, Query

from deps import Service

api_router = APIRouter()


@api_router.get("/search", status_code=status.HTTP_200_OK)
async def search(
        service: Service,
        search_query: str = Query(description="Запрос", example="Fight Club")

):
    return await service.search(search_query)
