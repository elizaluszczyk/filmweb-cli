import asyncio
from typing import TYPE_CHECKING

import click

from .client import FilmwebClient
from .display import Displayable, print_preview, print_search_results
from .services.info_service import InfoService
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

    search_results = asyncio.run(search_service.search(query))

    categories: list[tuple[str, Sequence[Displayable]]] = [
        ("FILMS", search_results.get_films()),
        ("SERIES", search_results.get_series()),
        ("GAMES", search_results.get_games()),
        ("CHARACTERS", search_results.get_characters()),
        ("PEOPLE", search_results.get_movie_people()),
        ("WORLDS", search_results.get_worlds()),
    ]

    print_search_results(categories)


@main.command("info")
@click.argument("content_id")
@click.pass_obj
def show_info(client: FilmwebClient, content_id: str) -> None:
    info_service = InfoService(client)

    content_info = asyncio.run(info_service.show_content_preview(int(content_id)))

    print_preview(content_info)


if __name__ == "__main__":
    main()
