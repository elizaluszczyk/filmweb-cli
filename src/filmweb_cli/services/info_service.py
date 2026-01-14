from typing import Annotated

from pydantic import Field, TypeAdapter

from filmweb_cli.client import FilmwebClient
from filmweb_cli.schemas.info.info import FilmInfo, GameInfo, SeriesInfo
from filmweb_cli.schemas.info.rating import ContentRating, Rating

ContentPreview = Annotated[FilmInfo | SeriesInfo | GameInfo, Field(discriminator="entity_name")]

NO_CONTENT_RESPONSE = 204


class InfoService:
    def __init__(self, client: FilmwebClient) -> None:
        self.client = client
        self.adapter = TypeAdapter(ContentPreview)

    async def show_content_preview(self, content_id: int) -> ContentPreview:
        info_response = await self.client.get(f"/film/{content_id}/preview")
        return self.adapter.validate_python(info_response.json())

    async def show_content_rating(self, content_id: int) -> ContentRating | None:
        rating_response = await self.client.get(f"/film/{content_id}/rating")
        if rating_response.status_code == NO_CONTENT_RESPONSE:
            return None

        return ContentRating.model_validate(rating_response.json())

    async def show_critics_content_rating(self, content_id: int) -> Rating | None:
        critics_rating_response = await self.client.get(f"/film/{content_id}/critics/rating")
        if critics_rating_response.status_code == NO_CONTENT_RESPONSE:
            return None

        return Rating.model_validate(critics_rating_response.json())
