from filmweb_cli.client import FilmwebClient
from filmweb_cli.schemas.search import (
    SearchCharacterResponse,
    SearchFilmResponse,
    SearchGameResponse,
    SearchPersonResponse,
    SearchSeriesResponse,
)


class SearchService:
    def __init__(self, client: FilmwebClient) -> None:
        self.client = client

    def search_film(self, query: str) -> SearchFilmResponse:
        search_film_response = self.client.get("/films/search", params={"query": query})
        return SearchFilmResponse.model_validate(search_film_response.json())

    def search_series(self, query: str) -> SearchSeriesResponse:
        search_series_response = self.client.get("/serials/search", params={"query": query})
        return SearchSeriesResponse.model_validate(search_series_response.json())

    def search_character(self, query: str) -> SearchCharacterResponse:
        search_character_response = self.client.get("/characters/search", params={"query": query})
        return SearchCharacterResponse.model_validate(search_character_response.json())

    def search_person(self, query: str) -> SearchPersonResponse:
        search_person_response = self.client.get("/persons/search", params={"query": query})
        return SearchPersonResponse.model_validate(search_person_response.json())

    def search_game(self, query: str) -> SearchGameResponse:
        search_game_response = self.client.get("/games/search", params={"query": query})
        return SearchGameResponse.model_validate(search_game_response.json())
