from rich.panel import Panel
from rich.table import Table

from filmweb_cli.schemas.info.worlds import WorldInfo

from .console import console
from .formatters import prettify_camel_case


def print_world_preview(info: WorldInfo) -> None:
    console.print(
        Panel(
            info.name,
            expand=False,
            border_style="dim",
        ),
    )

    if info.content_type_counts:
        console.print("[bold green]In this world:[/bold green]")

        for category, count in info.content_type_counts.items():
            table = Table(box=None, show_header=False, padding=(0, 1))
            table.add_column(style="dim cyan")
            table.add_column(style="bold")

            table.add_row(f"{prettify_camel_case(category)}:", str(count))

            console.print(table)
