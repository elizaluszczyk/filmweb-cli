from typing import TypeVar

from filmweb_cli.client import FilmwebClient
from filmweb_cli.schemas.search import SearchHit, SearchResponse

from .search_config import SEARCH_ENDPOINTS

T = TypeVar("T", bound=SearchHit)


class SearchService:
    def __init__(self, client: FilmwebClient) -> None:
        self.client = client

    def search(self, query: str, hit_type: type[T]) -> SearchResponse[T]:
        search_response = self.client.get(SEARCH_ENDPOINTS[hit_type], params={"query": query})
        return SearchResponse[hit_type].model_validate(search_response.json())
