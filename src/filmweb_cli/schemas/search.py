from typing import Generic, Literal, TypeVar

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


T = TypeVar("T", bound=SearchHit)


class SearchResponse(BaseModel, Generic[T]):
    total: int
    search_hits: list[T] = Field(alias="searchHits")
