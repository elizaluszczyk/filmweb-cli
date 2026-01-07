from typing import Literal

from pydantic import BaseModel, Field

from .cast import CastMember


class SearchHit(BaseModel):
    id: int
    matched_title: str | None = Field(default=None, alias="matchedTitle")
    matched_lang: str | None = Field(default=None, alias="matchedLang")
    film_main_cast: list[CastMember] | None = Field(default=None, alias="filmMainCast")


class SearchFilmHit(SearchHit):
    type: Literal["film"]


class SearchSeriesHit(SearchHit):
    type: Literal["serial"]


class SearchGameHit(SearchHit):
    type: Literal["game"]


class SearchCharacterHit(SearchHit):
    type: Literal["character"]
    matched_name: str = Field(alias="matchedName")


class SearchPersonHit(SearchHit):
    type: Literal["person"]


class SearchResponse(BaseModel):
    total: int


class SearchFilmResponse(SearchResponse):
    search_hits: list[SearchFilmHit] = Field(alias="searchHits")


class SearchSeriesResponse(SearchResponse):
    search_hits: list[SearchSeriesHit] = Field(alias="searchHits")


class SearchCharacterResponse(SearchResponse):
    search_hits: list[SearchCharacterHit] = Field(alias="searchHits")


class SearchPersonResponse(SearchResponse):
    search_hits: list[SearchPersonHit] = Field(alias="searchHits")


class SearchGameResponse(SearchResponse):
    search_hits: list[SearchGameHit] = Field(alias="searchHits")
