from pydantic import BaseModel, Field


class World(BaseModel):
    id: int
    name: str
    name_key: str | None = Field(default=None, alias="nameKey")


class WorldInfo(World):
    like_count: int | None = Field(default=None, alias="likeCount")
    content_type_counts: dict[str, int] | None = Field(default_factory=dict, alias="filmTypeCounts")
