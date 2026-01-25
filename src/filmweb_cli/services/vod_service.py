import httpx
from pydantic import TypeAdapter

from filmweb_cli.client import FilmwebClient
from filmweb_cli.exceptions.exceptions import InvalidContentError
from filmweb_cli.schemas.vod.vod_providers import ContentVodProvider, VodProvider

VOD_ADAPTER = TypeAdapter(list[VodProvider])
CONTENT_VOD_ADAPTER = TypeAdapter(list[ContentVodProvider])


class VodService:
    def __init__(self, client: FilmwebClient) -> None:
        self.client = client

    async def get_vod_providers(self) -> list[VodProvider]:
        vod_response = await self.client.get("/vod/providers/list")
        return VOD_ADAPTER.validate_python(vod_response.json())

    async def get_content_vod_providers(self, content_id: int) -> list[ContentVodProvider]:
        content_vod_response = await self.client.get(f"/vod/film/{content_id}/providers/list")

        self._validate_response(content_vod_response, content_id)

        return CONTENT_VOD_ADAPTER.validate_python(content_vod_response.json())

    @staticmethod
    def _validate_response(response: httpx.Response, resource_id: int) -> bool:
        if response.status_code == httpx.codes.OK:
            return True

        if response.status_code == httpx.codes.BAD_REQUEST:
            try:
                data = response.json()
                error_msg = data.get("message", "Type mismatch or malformed request")
            except (ValueError, AttributeError):
                error_msg = "Invalid request (could not parse error body)"

            msg = f"Filmweb API error ({resource_id}): {error_msg}"
            raise InvalidContentError(msg)

        response.raise_for_status()
        return True
