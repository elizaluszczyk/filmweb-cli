from typing import Annotated

from pydantic import BaseModel, Field

from .hits import SearchCharacterHit, SearchFilmHit, SearchGameHit, SearchPersonHit, SearchSeriesHit

SearchResult = Annotated[
    SearchFilmHit | SearchSeriesHit | SearchGameHit | SearchCharacterHit | SearchPersonHit,
    Field(discriminator="type"),
]


class SearchResponse(BaseModel):
    total: int
    search_hits: list[SearchResult] = Field(
        alias="searchHits",
    )

    def get_films(self) -> list[SearchFilmHit]:
        return [hit for hit in self.search_hits if isinstance(hit, SearchFilmHit)]

    def get_series(self) -> list[SearchSeriesHit]:
        return [hit for hit in self.search_hits if isinstance(hit, SearchSeriesHit)]

    def get_games(self) -> list[SearchGameHit]:
        return [hit for hit in self.search_hits if isinstance(hit, SearchGameHit)]

    def get_characters(self) -> list[SearchCharacterHit]:
        return [hit for hit in self.search_hits if isinstance(hit, SearchCharacterHit)]

    def get_movie_people(self) -> list[SearchPersonHit]:
        return [hit for hit in self.search_hits if isinstance(hit, SearchPersonHit)]
