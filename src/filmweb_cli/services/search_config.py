from filmweb_cli.schemas.search import (
    SearchCharacterHit,
    SearchFilmHit,
    SearchGameHit,
    SearchHit,
    SearchPersonHit,
    SearchSeriesHit,
)

SEARCH_ENDPOINTS: dict[type[SearchHit], str] = {
    SearchFilmHit: "/films/search",
    SearchSeriesHit: "/serials/search",
    SearchCharacterHit: "/characters/search",
    SearchPersonHit: "/persons/search",
    SearchGameHit: "/games/search",
}
