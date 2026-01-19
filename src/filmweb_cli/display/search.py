from collections.abc import Sequence
from typing import Protocol

from rich.table import Table

from filmweb_cli.display.console import console


class Displayable(Protocol):
    def display_name(self) -> str: ...
    def get_id(self) -> str: ...


def print_search_results(categories: list[tuple[str, Sequence[Displayable]]]) -> None:
    has_results = False
    for name, items in categories:
        if not items:
            continue
        has_results = True

        console.print(f"[bold cyan]{name}[/bold cyan]")
        table = Table(box=None, show_header=False, padding=(0, 2))
        table.add_column(style="dim", width=3)
        table.add_column()

        for i, item in enumerate(items, 1):
            table.add_row(str(i), item.display_name(), item.get_id())

        console.print(table)
        console.print()

    if not has_results:
        console.print("[dim]No results found.[/dim]")
