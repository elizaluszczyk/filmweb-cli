from pydantic import BaseModel, Field


class World(BaseModel):
    id: int
    name: str
    name_key: str | None = Field(default=None, alias="nameKey")
