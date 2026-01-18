import asyncio
from typing import TYPE_CHECKING

import click

from .client import FilmwebClient
from .display import (
    Displayable,
    print_preview,
    print_search_results,
    print_where_to_watch,
    print_where_to_watch_compact,
)
from .schemas.vod.vod_providers import WhereToWatch
from .services.info_service import InfoService
from .services.search_service import SearchService
from .services.vod_service import VodService

if TYPE_CHECKING:
    from collections.abc import Sequence


@click.group()
@click.pass_context
def main(ctx: click.Context) -> None:
    ctx.obj = FilmwebClient()


@main.command("search")
@click.argument("query")
@click.option("--raw", is_flag=True, hidden=True, help="Output raw format")
@click.pass_obj
def search(client: FilmwebClient, query: str, *, raw: bool) -> None:
    search_service = SearchService(client)
    search_results = asyncio.run(search_service.search(query))

    if raw:
        for category, items in [
            ("FILM", search_results.get_films()),
            ("SERIES", search_results.get_series()),
            ("GAME", search_results.get_games()),
            ("CHARACTER", search_results.get_characters()),
            ("PERSON", search_results.get_movie_people()),
            ("WORLD", search_results.get_worlds()),
        ]:
            for item in items:
                click.echo(f"{item.get_id()}\t[{category}] {item.display_name()}")
    else:
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
    async def fetch_info() -> tuple:
        info_service = InfoService(client)
        content_info = await info_service.show_content_preview(int(content_id))
        rating_info = await info_service.show_content_rating(int(content_id))
        critics_rating_info = await info_service.show_critics_content_rating(int(content_id))
        return content_info, rating_info, critics_rating_info

    content_info, rating_info, critics_rating_info = asyncio.run(fetch_info())
    print_preview(content_info, rating_info, critics_rating_info)


@main.command("vod")
@click.argument("content_id")
@click.option("--compact", "-c", is_flag=True, hidden=True, help="Compact display of vod providers")
@click.pass_obj
def show_vod_providers(client: FilmwebClient, content_id: str, *, compact: bool) -> None:
    async def fetch_info() -> tuple:
        vod_service = VodService(client)
        vod_providers = await vod_service.get_vod_providers()
        content_vod_providers = await vod_service.get_content_vod_providers(int(content_id))
        return vod_providers, content_vod_providers

    vod_providers, content_vod_providers = asyncio.run(fetch_info())

    vod_providers_by_id = {p.id: p for p in vod_providers}

    where_to_watch_list: list[WhereToWatch] = [
        WhereToWatch(
            content=cp,
            provider=vod_providers_by_id.get(cp.vod_provider),
        )
        for cp in content_vod_providers
    ]

    if compact:
        print_where_to_watch_compact(where_to_watch_list)
    else:
        print_where_to_watch(where_to_watch_list)


if __name__ == "__main__":
    main()
