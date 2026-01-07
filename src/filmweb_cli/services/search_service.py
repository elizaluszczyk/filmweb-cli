from filmweb_cli.client import FilmwebClient
from filmweb_cli.schemas.search import SearchFilmResponse, SearchSeriesResponse


class SearchService:
    def __init__(self, client: FilmwebClient) -> None:
        self.client = client

    def search_film(self, query: str) -> SearchFilmResponse:
        search_film_response = self.client.get("/films/search", params={"query": query})
        return SearchFilmResponse.model_validate(search_film_response.json())

    def search_series(self, query: str) -> SearchSeriesResponse:
        search_series_response = self.client.get("/serials/search", params={"query": query})
        return SearchSeriesResponse.model_validate(search_series_response.json())
