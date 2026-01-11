from typing import Annotated

from pydantic import Field, TypeAdapter

from filmweb_cli.client import FilmwebClient
from filmweb_cli.schemas.info.info import FilmInfo, GameInfo, SeriesInfo

ContentPreview = Annotated[FilmInfo | SeriesInfo | GameInfo, Field(discriminator="entity_name")]


class InfoService:
    def __init__(self, client: FilmwebClient) -> None:
        self.client = client
        self.adapter = TypeAdapter(ContentPreview)

    async def show_content_preview(self, content_id: int) -> ContentPreview:
        info_response = await self.client.get(f"/film/{content_id}/preview")
        return self.adapter.validate_python(info_response.json())
