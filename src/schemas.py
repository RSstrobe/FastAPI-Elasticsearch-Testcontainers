from pydantic import BaseModel, Field


class MoviesSchema(BaseModel):
    imdb_rating: float | None = Field(description="Рейтинг произведения")
    genres: list[str] = Field(description="Имена жанров c id")
    title: str = Field(description="Наименование произведения")
    description: str = Field(description="Описание произведения")
