from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field

from .cast import CastMember


class SearchHit(BaseModel):
    id: int

    def display_name(self) -> str:
        return str(self.id)


class SearchContent(SearchHit):
    matched_title: str = Field(alias="matchedTitle")
    matched_lang: str = Field(alias="matchedLang")
    main_cast: list[CastMember] = Field(default_factory=list, alias="filmMainCast")

    def display_name(self) -> str:
        return self.matched_title


class SearchFilmHit(SearchContent):
    type: Literal["film"]


class SearchSeriesHit(SearchContent):
    type: Literal["serial"]


class SearchGameHit(SearchContent):
    type: Literal["game"]


class SearchCharacterHit(SearchHit):
    type: Literal["character"]
    matched_name: str = Field(alias="matchedName")

    def display_name(self) -> str:
        return self.matched_name


class SearchPersonHit(SearchHit):
    type: Literal["person"]


T = TypeVar("T", bound=SearchHit)


class SearchResponse(BaseModel, Generic[T]):
    total: int
    search_hits: list[T] = Field(alias="searchHits")
