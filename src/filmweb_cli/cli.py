from typing import TYPE_CHECKING

import click

from .client import FilmwebClient
from .display import Displayable, print_search_results
from .services.search_service import SearchService

if TYPE_CHECKING:
    from collections.abc import Sequence


@click.group()
@click.pass_context
def main(ctx: click.Context) -> None:
    ctx.obj = FilmwebClient()


@main.command("search")
@click.argument("query")
@click.pass_obj
def search(client: FilmwebClient, query: str) -> None:
    search_service = SearchService(client)

    search_results = search_service.search(query)

    categories: list[tuple[str, Sequence[Displayable]]] = [
        ("FILMS", search_results.get_films()),
        ("SERIES", search_results.get_series()),
        ("GAMES", search_results.get_games()),
        ("CHARACTERS", search_results.get_characters()),
        ("PEOPLE", search_results.get_movie_people()),
    ]

    print_search_results(categories)


if __name__ == "__main__":
    main()
