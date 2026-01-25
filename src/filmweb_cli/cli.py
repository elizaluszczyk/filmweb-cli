import asyncio
from typing import TYPE_CHECKING

import click

from .client import FilmwebClient
from .display.character_preview import print_character_preview
from .display.content_preview import print_content_preview
from .display.people_preview import print_person_preview
from .display.search import print_search_results
from .display.vod import print_where_to_watch, print_where_to_watch_compact
from .display.worlds_preview import print_world_preview
from .exceptions.exceptions import ContentNotFoundError, InvalidContentError, InvalidIdTypeException
from .schemas.vod.vod_providers import WhereToWatch
from .services.info_service import InfoService
from .services.search_service import SearchService
from .services.vod_service import VodService

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .display.search import Displayable

VALID_CONTENT_TYPES = {"film", "series", "game", "person", "character", "world"}
MEDIA_TYPES = {"film", "series", "game"}
VOD_TYPES = {"film", "series"}


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
        for type_prefix, category, items in [
            ("film", "FILM", search_results.get_films()),
            ("series", "SERIES", search_results.get_series()),
            ("game", "GAME", search_results.get_games()),
            ("character", "CHARACTER", search_results.get_characters()),
            ("person", "PERSON", search_results.get_movie_people()),
            ("world", "WORLD", search_results.get_worlds()),
        ]:
            for item in items:
                click.echo(f"{type_prefix}:{item.get_id()}\t[{category}] {item.display_name()}")
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
@click.option("--full", "-f", is_flag=True, hidden=True, help="Show full description")
@click.pass_obj
def show_info(client: FilmwebClient, content_id: str, *, full: bool) -> None:
    info_service = InfoService(client)

    try:
        parsed_type, parsed_id = _parse_content_input(content_id)
    except InvalidIdTypeException as e:
        click.echo(e, err=True)
        raise SystemExit(1) from e

    try:
        if parsed_type in MEDIA_TYPES:
            content_info, rating_info, critics_rating_info, full_description_info = asyncio.run(
                _fetch_media_info(info_service, parsed_id, full=full),
            )

            print_content_preview(
                content_info,
                rating_info,
                critics_rating_info,
                full_description_info,
                full_desc=full,
            )

        elif parsed_type == "person":
            person_info = asyncio.run(info_service.get_person_preview(parsed_id))
            print_person_preview(person_info)

        elif parsed_type == "character":
            character_info, content_info = asyncio.run(_fetch_character_info(info_service, parsed_id))
            print_character_preview(character_info, content_info)

        elif parsed_type == "world":
            person_info = asyncio.run(info_service.get_world_preview(parsed_id))
            print_world_preview(person_info)

        else:
            click.echo(f"Unsupported content type: {parsed_type}")
            raise SystemExit(1)

    except ContentNotFoundError as e:
        click.echo(e, err=True)
        raise SystemExit(1) from e
    except InvalidContentError as e:
        click.echo(e, err=True)
        raise SystemExit(1) from e


async def _fetch_media_info(info_service: InfoService, content_id: int, *, full: bool) -> tuple:
    desc_task = None

    async with asyncio.TaskGroup() as tg:
        preview_task = tg.create_task(info_service.get_content_preview(content_id))
        rating_task = tg.create_task(info_service.get_content_rating(content_id))
        critics_rating_task = tg.create_task(info_service.get_critics_content_rating(content_id))

        if full:
            desc_task = tg.create_task(info_service.get_full_description(content_id))

    desc = desc_task.result() if desc_task is not None else None

    return (
        preview_task.result(),
        rating_task.result(),
        critics_rating_task.result(),
        desc,
    )


async def _fetch_character_info(info_service: InfoService, character_id: int) -> tuple:
    async with asyncio.TaskGroup() as tg:
        preview_task = tg.create_task(info_service.get_character_preview(character_id))
        content_task = tg.create_task(info_service.get_character_content(character_id))

    return (preview_task.result(), content_task.result())


@main.command("vod")
@click.argument("content_id")
@click.option("--compact", "-c", is_flag=True, hidden=True, help="Compact display of vod providers")
@click.pass_obj
def show_vod_providers(client: FilmwebClient, content_id: str, *, compact: bool) -> None:
    try:
        parsed_type, parsed_id = _parse_content_input(content_id)

        if parsed_type not in VOD_TYPES:
            raise SystemExit(0)

        async def fetch_info() -> tuple:
            vod_service = VodService(client)
            return await asyncio.gather(
                vod_service.get_vod_providers(),
                vod_service.get_content_vod_providers(parsed_id),
            )

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

    except InvalidContentError as e:
        click.echo(e, err=True)
        raise SystemExit(1) from e


def _parse_content_input(content_id: str) -> tuple[str, int]:
    if ":" in content_id:
        type_prefix, numeric_id = content_id.split(":", 1)

        if type_prefix not in VALID_CONTENT_TYPES:
            click.echo(f"Unknkown prefix: {type_prefix}.")
            click.echo(f"Available: {', '.join(VALID_CONTENT_TYPES)}")
            raise SystemExit(1)

        if not numeric_id.isdecimal():
            msg = f"Invalid id type: {numeric_id} should be a number"
            raise InvalidIdTypeException(msg)

        return type_prefix, int(numeric_id)

    return "film", int(content_id)


if __name__ == "__main__":
    main()
