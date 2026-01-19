from typing import Literal

from pydantic import BaseModel, Field

from filmweb_cli.schemas.people import Person


class SearchHit(BaseModel):
    id: int

    def get_id(self) -> str:
        return str(self.id)


class SearchContent(SearchHit):
    matched_title: str = Field(alias="matchedTitle")
    matched_lang: str | None = Field(default=None, alias="matchedLang")
    main_cast: list[Person] = Field(default_factory=list, alias="filmMainCast")

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
    person_know_for: int = Field(alias="personKnowFor")
    person_main_profession: str = Field(alias="personMainProfession")

    full_name: str | None = None

    def display_name(self) -> str:
        return self.full_name or f"Person: {self.id!s}"


class SearchWorldHit(SearchHit):
    type: Literal["world"]
    matched_lang: str = Field(alias="matchedLang")
    matched_name: str = Field(alias="matchedName")

    def display_name(self) -> str:
        return self.matched_name
