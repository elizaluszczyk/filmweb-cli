import asyncio

from filmweb_cli.client import FilmwebClient
from filmweb_cli.schemas.people import Person
from filmweb_cli.schemas.search.response import SearchPersonHit, SearchResponse


class SearchService:
    def __init__(self, client: FilmwebClient) -> None:
        self.client = client

    async def search(self, query: str) -> SearchResponse:
        search_raw_response = await self.client.get("/live/search", params={"query": query})
        response = SearchResponse.model_validate(search_raw_response.json())

        await self._fetch_person_details(response)

        return response

    async def _fetch_person_details(self, response: SearchResponse) -> None:
        tasks = []
        person_hits: list[SearchPersonHit] = []

        for hit in response.search_hits:
            if isinstance(hit, SearchPersonHit):
                person_hits.append(hit)
                tasks.append(self._get_person_name(hit.id))

        if not tasks:
            return

        details = await asyncio.gather(*tasks)

        for person_hit, person_details in zip(person_hits, details, strict=True):
            person_hit.full_name = person_details.name

    async def _get_person_name(self, person_id: int) -> Person:
        person_response = await self.client.get(f"/person/{person_id}/info")
        return Person.model_validate(person_response.json())
