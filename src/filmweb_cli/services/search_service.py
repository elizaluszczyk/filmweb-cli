from filmweb_cli.client import FilmwebClient
from filmweb_cli.schemas.search.response import SearchResponse


class SearchService:
    def __init__(self, client: FilmwebClient) -> None:
        self.client = client

    def search(self, query: str) -> SearchResponse:
        search_response = self.client.get("/live/search", params={"query": query})
        return SearchResponse.model_validate(search_response.json())
