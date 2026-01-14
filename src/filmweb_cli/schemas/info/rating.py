from pydantic import BaseModel, Field


class ContentRating(BaseModel):
    count: int
    rate: float
    count_want_to_see: int = Field(alias="countWantToSee")
    count_vote_1: int = Field(alias="countVote1")
    count_vote_2: int = Field(alias="countVote2")
    count_vote_3: int = Field(alias="countVote3")
    count_vote_4: int = Field(alias="countVote4")
    count_vote_5: int = Field(alias="countVote5")
    count_vote_6: int = Field(alias="countVote6")
    count_vote_7: int = Field(alias="countVote7")
    count_vote_8: int = Field(alias="countVote8")
    count_vote_9: int = Field(alias="countVote9")
    count_vote_10: int = Field(alias="countVote10")
