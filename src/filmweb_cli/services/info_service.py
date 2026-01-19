import asyncio
from typing import Annotated

from pydantic import Field, TypeAdapter

from filmweb_cli.client import FilmwebClient
from filmweb_cli.schemas.info.content_info import FilmInfo, FullDescription, GameInfo, SeriesInfo
from filmweb_cli.schemas.info.people_characters_info import PersonInfo
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

    async def get_person_preview(self, person_id: int) -> PersonInfo:
        person_raw_response = await self.client.get(f"/person/{person_id}/preview")
        response = PersonInfo.model_validate(person_raw_response.json())

        await self._fetch_person_content(response)

        return response

    async def _fetch_person_content(self, response: PersonInfo) -> None:
        tasks = [self.get_content_preview(content_id) for content_id in response.content_known_for]

        if not tasks:
            return

        details = await asyncio.gather(*tasks)

        titles: list[str] = []

        for item in details:
            title = item.title.title if item.title else item.original_title.title
            titles.append(title)

        response.known_for_titles = titles
