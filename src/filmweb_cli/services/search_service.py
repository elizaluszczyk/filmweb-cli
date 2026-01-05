from filmweb_cli.client import FilmwebClient
from filmweb_cli.schemas.search import SearchResponse


class SearchService:
    def __init__(self, client: FilmwebClient) -> None:
        self.client = client

    def search(self, query: str, page_size: int = 10) -> SearchResponse:
        search_response = self.client.get("/live/search", params={"query": query, "pageSize": page_size})
        return SearchResponse.model_validate(search_response.json())
