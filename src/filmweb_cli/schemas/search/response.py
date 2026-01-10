from pydantic import BaseModel, Field

from .hits import SearchCharacterHit, SearchFilmHit, SearchGameHit, SearchPersonHit, SearchSeriesHit


class SearchResponse(BaseModel):
    total: int
    search_hits: list[SearchFilmHit | SearchSeriesHit | SearchGameHit | SearchCharacterHit | SearchPersonHit] = Field(
        alias="searchHits",
    )
