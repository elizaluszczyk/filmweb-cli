import click

from .client import FilmwebClient
from .services.search_service import SearchService


@click.group()
@click.pass_context
def main(ctx: click.Context) -> None:
    client = FilmwebClient()
    ctx.obj = client


@main.group("search")
def search() -> None:
    pass


@search.command("film")
@click.argument("query")
@click.pass_obj
def film(client: FilmwebClient, query: str) -> None:
    search_service = SearchService(client)

    search_film_results = search_service.search_film(query)

    for film in search_film_results.search_hits:
        click.echo(film.matched_title)


@search.command("series")
@click.argument("query")
@click.pass_obj
def series(client: FilmwebClient, query: str) -> None:
    search_service = SearchService(client)

    search_series_results = search_service.search_series(query)

    for series in search_series_results.search_hits:
        click.echo(series.matched_title)


if __name__ == "__main__":
    main()
