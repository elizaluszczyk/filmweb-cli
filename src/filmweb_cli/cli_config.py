from .schemas.search import (
    SearchCharacterHit,
    SearchFilmHit,
    SearchGameHit,
    SearchHit,
    SearchPersonHit,
    SearchSeriesHit,
)

SEARCH_COMMAND: dict[str, SearchHit] = {
    "film": SearchFilmHit,
    "series": SearchSeriesHit,
    "character": SearchCharacterHit,
    "person": SearchPersonHit,
    "game": SearchGameHit,
}
