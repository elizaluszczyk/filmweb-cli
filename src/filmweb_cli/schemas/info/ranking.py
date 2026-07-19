from pydantic import BaseModel, Field


class Top(BaseModel):
    id: int
    count: int
    rate: float


class TopRole(Top):
    person_id: int = Field(alias="person")
    profession: str | None = None

    person_name: str | None = None
