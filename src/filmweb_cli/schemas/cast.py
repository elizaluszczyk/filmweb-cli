from pydantic import BaseModel


class CastMember(BaseModel):
    id: int
    name: str
