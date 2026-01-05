from typing import Literal

from pydantic import BaseModel, Field

from .cast import CastMember


class SearchHit(BaseModel):
    id: int
    type: Literal["film", "serial"]
    matched_title: str = Field(alias="matchedTitle")
    matched_lang: str = Field(alias="matchedLang")
    film_main_cast: list[CastMember] = Field(alias="filmMainCast")


class SearchResponse(BaseModel):
    total: int
    search_hits: list[SearchHit] = Field(alias="searchHits")
