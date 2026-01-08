import click

from .cli_config import SEARCH_COMMAND
from .client import FilmwebClient
from .schemas.search import SearchHit
from .services.search_service import SearchService


@click.group()
@click.pass_context
def main(ctx: click.Context) -> None:
    ctx.obj = FilmwebClient()


@main.group("search")
def search() -> None:
    pass


def make_search_command(hit_type: SearchHit) -> None:

    @click.argument("query")
    @click.pass_obj
    def command(client: FilmwebClient, query: str) -> None:
        search_service = SearchService(client)

        search_results = search_service.search(query, hit_type)

        for result in search_results.search_hits:
            click.echo(result.matched_title or "no title")

    return command


for name, hit_type in SEARCH_COMMAND.items():
    search.command(name)(make_search_command(hit_type))


if __name__ == "__main__":
    main()
