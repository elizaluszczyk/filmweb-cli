from pydantic import BaseModel, Field


class Rating(BaseModel):
    count: int
    rate: float


class ContentRating(Rating):
    count_want_to_see: int = Field(alias="countWantToSee")
    count_vote_1: int | None = Field(default=None, alias="countVote1")
    count_vote_2: int | None = Field(default=None, alias="countVote2")
    count_vote_3: int | None = Field(default=None, alias="countVote3")
    count_vote_4: int | None = Field(default=None, alias="countVote4")
    count_vote_5: int | None = Field(default=None, alias="countVote5")
    count_vote_6: int | None = Field(default=None, alias="countVote6")
    count_vote_7: int | None = Field(default=None, alias="countVote7")
    count_vote_8: int | None = Field(default=None, alias="countVote8")
    count_vote_9: int | None = Field(default=None, alias="countVote9")
    count_vote_10: int | None = Field(default=None, alias="countVote10")
