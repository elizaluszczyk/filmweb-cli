from collections.abc import Sequence
from typing import Protocol

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from filmweb_cli.schemas.info.info import ContentInfo
from filmweb_cli.schemas.info.rating import ContentRating

console = Console(width=80, highlight=False)

THOUSAND_THRESHOLD = 1000


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

    console.print(Panel(
        f"[dim cyan]{_build_metadata_line(info)}[/dim cyan]",
        title=_build_panel_title(title, original),
        title_align="left",
        expand=False,
        border_style="dim",
    ))

    if rating:
        console.print(
            f"[bold magenta]★ {rating.rate:.1f}[/bold magenta]"
            f"[dim] · {_format_count(rating.count)}[/dim]",
        )

    if info.directors:
        console.print(f"[bold]Directors:[/bold] {_join_names(info.directors)}")

    if info.main_cast:
        console.print(f"[bold]Main cast:[/bold] {_join_names(info.main_cast)}")

    if info.description:
        console.print()
        console.print(info.description)


def _format_count(count: int) -> str:
    return f"{count / 1000:.0f} tys" if count >= THOUSAND_THRESHOLD else str(count)


def _join_names(items: list) -> str:
    return ", ".join(item.name for item in items)


def _build_panel_title(title: str, original: str) -> str:
    panel_title = f"[bold]{title}[/bold]"
    if title != original:
        panel_title += f" / [dim]{original}[/dim]"
    return panel_title


def _build_metadata_line(info: ContentInfo) -> str:
    metadata = [
        str(info.year) if info.year else None,
        f"{info.duration} min" if info.duration else None,
        _join_names(info.genres) if info.genres else None,
    ]
    return " · ".join(filter(None, metadata))
