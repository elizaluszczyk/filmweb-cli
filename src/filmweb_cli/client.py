import httpx


class FilmwebClient:
    def __init__(self) -> None:
        self.api_base = "https://www.filmweb.pl/api/v1"
        self.client = httpx.Client()

    def get(self, endpoint: str, **kwargs: dict) -> httpx.Response:
        return self.client.get(self.api_base + endpoint, **kwargs)
