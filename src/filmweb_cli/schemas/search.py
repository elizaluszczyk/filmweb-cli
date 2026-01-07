from typing import Literal

from pydantic import BaseModel, Field

from .cast import CastMember


class SearchHit(BaseModel):
    id: int
    type: Literal["film", "serial"]
    matched_title: str = Field(alias="matchedTitle")
    matched_lang: str = Field(alias="matchedLang")
    film_main_cast: list[CastMember] | None = Field(default=None, alias="filmMainCast")


class SearchFilmHit(SearchHit):
    type: Literal["film"]


class SearchSeriesHit(SearchHit):
    type: Literal["serial"]


class SearchFilmResponse(BaseModel):
    total: int
    search_hits: list[SearchFilmHit] = Field(alias="searchHits")


class SearchSeriesResponse(BaseModel):
    total: int
    search_hits: list[SearchSeriesHit] = Field(alias="searchHits")
