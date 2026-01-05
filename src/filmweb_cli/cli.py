import click

from .client import FilmwebClient
from .services.search_service import SearchService


@click.group()
@click.pass_context
def main(ctx: click.Context) -> None:
    client = FilmwebClient()
    ctx.obj = client


@main.command("search")
@click.argument("query")
@click.pass_obj
def search(client: FilmwebClient, query: str) -> None:
    search_service = SearchService(client)

    search_results = search_service.search(query)

    for result in search_results.search_hits:
        click.echo(result)


if __name__ == "__main__":
    main()
