import httpx


class FilmwebClient:
    def __init__(self) -> None:
        self.api_base = "https://www.filmweb.pl/api/v1"
        self.ajax_api_base = "https://www.filmweb.pl/ajax"
        self.client = httpx.AsyncClient()

    async def _get(self, base_url: str, endpoint: str, **kwargs: dict) -> httpx.Response:
        return await self.client.get(base_url + endpoint, **kwargs)

    async def get(self, endpoint: str, **kwargs: dict) -> httpx.Response:
        return await self._get(self.api_base, endpoint, **kwargs)

    async def get_ajax(self, endpoint: str, **kwargs: dict) -> httpx.Response:
        return await self._get(self.ajax_api_base, endpoint, **kwargs)
