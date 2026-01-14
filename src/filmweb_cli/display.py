from collections.abc import Sequence
from typing import Protocol

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from filmweb_cli.schemas.info.info import ContentInfo
from filmweb_cli.schemas.info.rating import ContentRating

console = Console(width=80, highlight=False)


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


def print_preview(info: ContentInfo, rating: ContentRating) -> None:
    title = info.title.title if info.title else info.original_title.title
    original = info.original_title.title

    panel_title = f"[bold]{title}[/bold]"
    if title != original:
        panel_title += f" / [dim]{original}[/dim]"

    genres = ", ".join(g.name for g in info.genres)

    data = []

    if info.year:
        data.append(str(info.year))

    if info.duration:
        data.append(f"{info.duration} min")

    if genres:
        data.append(genres)

    data_text = " · ".join(data)
    panel_content = f"[dim cyan]{data_text}[/dim cyan]"

    console.print(Panel(panel_content, title=panel_title, title_align="left", expand=False, border_style="dim"))

    if rating:
        count_display = f"{rating.count}" if rating.count < 1000 else f"{rating.count / 1000:.0f} tys"
        console.print(f"[bold magenta]★ {rating.rate:.1f}[/bold magenta][dim] · {count_display}[/dim]")

    if info.directors:
        console.print(f"[bold]Directors:[/bold] {', '.join(d.name for d in info.directors)}")

    if info.main_cast:
        console.print(f"[bold]Main cast:[/bold] {', '.join(p.name for p in info.main_cast)}")

    if info.description:
        console.print()
        console.print(info.description)
