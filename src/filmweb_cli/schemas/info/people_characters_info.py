from pydantic import BaseModel, Field

from .worlds import World


class PersonalDetails(BaseModel):
    real_name: str | None = Field(default=None, alias="realName")
    height: int | None = None
    birth_date_int: int | None = Field(default=None, alias="birthDateInt")
    death_date_int: int | None = Field(default=None, alias="deathDateInt")


class BirthPlace(BaseModel):
    country: int | None = None
    city_name: str | None = Field(default=None, alias="cityName")
    region_name: str | None = Field(default=None, alias="regionName")


class CharacterTypeName(BaseModel):
    text: str | None = None
    lang: str | None = None


class CharacterType(BaseModel):
    id: int
    name: CharacterTypeName
    name_key: str | None = Field(default=None, alias="nameKey")


class FigureInfo(BaseModel):
    id: int
    name: str
    sex: int


class PersonInfo(FigureInfo):  # not all information from api response is parsed here
    details: PersonalDetails | None = Field(default=None, alias="info")
    birthplace: BirthPlace | None = None
    content_known_for: list[int] = Field(default_factory=list, alias="filmsKnownFor")
    main_profession: str | None = Field(default=None, alias="mainProfession")

    known_for_titles: list[str] = Field(default_factory=list)


class CharacterInfo(FigureInfo):  # not all information from api response is parsed here
    real_name: str | None = Field(default=None, alias="realName")
    like_count: int | None = Field(default=None, alias="likeCount")
    world: World | None = None
    types: list[CharacterType] = Field(default_factory=list)
    real_name_key: str | None = Field(default=None, alias="realNameKey")
    name_key: str | None = Field(default=None, alias="nameKey")


class CharacterContentResponse(BaseModel):
    content_known_for: dict[str, list[int]] = Field(default_factory=dict, alias="filmTypeFilmIds")
    main_request_type: str = Field(alias="mainRequestType")

    known_for_titles: dict[str, list[str]] = Field(default_factory=dict)
