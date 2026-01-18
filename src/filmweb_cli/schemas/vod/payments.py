from pydantic import BaseModel, Field


class Payment(BaseModel):  # not all information from api response is parsed here
    film_vod: int = Field(alias="filmVod")
    price: int
    buy: bool
    rent: bool
    free: bool
    subscription: bool
    internet_tv: bool = Field(alias="internetTv")
