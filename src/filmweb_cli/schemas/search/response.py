from typing import Annotated

from pydantic import BaseModel, Field, model_validator

from .hits import SearchCharacterHit, SearchFilmHit, SearchGameHit, SearchPersonHit, SearchSeriesHit, SearchWorldHit

SearchResult = Annotated[
    SearchFilmHit | SearchSeriesHit | SearchGameHit | SearchCharacterHit | SearchPersonHit | SearchWorldHit,
    Field(discriminator="type"),
]

ALLOWED_TYPES = {"film", "serial", "game", "person", "character", "world"}


class SearchResponse(BaseModel):
    total: int
    search_hits: list[SearchResult] = Field(alias="searchHits")

    @model_validator(mode="before")
    @classmethod
    def filter_unknown_types(cls, data: dict) -> dict:
        if "searchHits" in data:
            data["searchHits"] = [
                hit for hit in data["searchHits"]
                if hit.get("type") in ALLOWED_TYPES
            ]
        return data

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

    def get_worlds(self) -> list[SearchWorldHit]:
        return [hit for hit in self.search_hits if isinstance(hit, SearchWorldHit)]
