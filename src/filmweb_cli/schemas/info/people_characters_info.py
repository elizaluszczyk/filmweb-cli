from pydantic import BaseModel, Field


class PersonalDetails(BaseModel):
    real_name: str | None = Field(default=None, alias="realName")
    height: int | None = None
    birth_date_int: int | None = Field(default=None, alias="birthDateInt")


class BirthPlace(BaseModel):
    country: int | None = None
    city_name: str | None = Field(default=None, alias="cityName")
    region_name: str | None = Field(default=None, alias="regionName")


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
