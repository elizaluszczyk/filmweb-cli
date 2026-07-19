import asyncio

from pydantic import TypeAdapter

from filmweb_cli.client import FilmwebClient
from filmweb_cli.schemas.info.ranking import TopRole

from .base_service import BaseService
from .info_service import InfoService

TOP_ROLE_ADAPTER = TypeAdapter(list[TopRole])


class RankingService(BaseService):
    def __init__(self, client: FilmwebClient) -> None:
        self.client = client

    async def get_content_top_roles(self, content_id: int) -> list[TopRole] | None:
        top_roles_response = await self.client.get(f"/film/{content_id}/top-roles")

        if not self._validate_response(top_roles_response, content_id, allow_missing=True):
            return None

        response = TOP_ROLE_ADAPTER.validate_python(top_roles_response.json())

        await self._fetch_top_role_person(response)

        return response

    async def _fetch_top_role_person(self, roles: list[TopRole]) -> None:
        info_service = InfoService(self.client)
        tasks = [info_service.get_person_preview(role.person_id) for role in roles]

        if not tasks:
            return

        details = await asyncio.gather(*tasks)

        for role, person_details in zip(roles, details, strict=True):
            if person_details:
                role.person_name = person_details.name
