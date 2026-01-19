from pydantic import BaseModel, Field

from .payments import Payment


class VodProvider(BaseModel):  # not all information from api response is parsed here
    id: int
    name: str
    display_name: str = Field(alias="displayName")
    link: str | None = None


class ContentVodProvider(BaseModel):  # not all information from api response is parsed here
    vod_provider: int = Field(alias="vodProvider")
    id: int
    film: int
    start: str
    link: str | None = None
    payments: list[Payment] = Field(default_factory=list)


class WhereToWatch(BaseModel):
    content: ContentVodProvider
    provider: VodProvider | None = None
