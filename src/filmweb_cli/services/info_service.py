from typing import Annotated

from pydantic import Field, TypeAdapter

from filmweb_cli.client import FilmwebClient
from filmweb_cli.schemas.info.info import FilmInfo, FullDescription, GameInfo, SeriesInfo
from filmweb_cli.schemas.info.rating import ContentRating, Rating

ContentPreview = Annotated[FilmInfo | SeriesInfo | GameInfo, Field(discriminator="entity_name")]
CONTENT_PREVIEW_ADAPTER = TypeAdapter(ContentPreview)

NO_CONTENT_RESPONSE = 204


class InfoService:
    def __init__(self, client: FilmwebClient) -> None:
        self.client = client

    async def get_content_preview(self, content_id: int) -> ContentPreview:
        info_response = await self.client.get(f"/film/{content_id}/preview")
        return CONTENT_PREVIEW_ADAPTER.validate_python(info_response.json())

    async def get_content_rating(self, content_id: int) -> ContentRating | None:
        rating_response = await self.client.get(f"/film/{content_id}/rating")
        if rating_response.status_code == NO_CONTENT_RESPONSE:
            return None

        return ContentRating.model_validate(rating_response.json())

    async def get_critics_content_rating(self, content_id: int) -> Rating | None:
        critics_rating_response = await self.client.get(f"/film/{content_id}/critics/rating")
        if critics_rating_response.status_code == NO_CONTENT_RESPONSE:
            return None

        return Rating.model_validate(critics_rating_response.json())

    async def get_full_description(self, content_id: int) -> FullDescription:
        description_response = await self.client.get(f"/film/{content_id}/description")
        return FullDescription.model_validate(description_response.json())
