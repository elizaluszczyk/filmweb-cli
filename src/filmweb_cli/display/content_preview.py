from rich.panel import Panel

from filmweb_cli.display.console import console
from filmweb_cli.schemas.info.content_info import ContentInfo, FullDescription
from filmweb_cli.schemas.info.rating import ContentRating, Rating

THOUSAND_THRESHOLD = 1000


def print_content_preview(
    info: ContentInfo, rating: ContentRating, critics_rating: Rating, description: FullDescription, *, full_desc: bool,
) -> None:
    title = info.title.title if info.title else info.original_title.title
    original = info.original_title.title

    console.print(
        Panel(
            f"[dim cyan]{_build_metadata_line(info)}[/dim cyan]",
            title=_build_panel_title(title, original),
            title_align="left",
            expand=False,
            border_style="dim",
        ),
    )

    if rating and rating.count is not None:
        console.print(
            f"[bold magenta]★ {rating.rate:.1f}[/bold magenta][dim] · {_format_count(rating.count)}[/dim]",
        )

    if critics_rating:
        console.print(
            f"[bold green]☆ {critics_rating.rate:.1f}[/bold green][dim] · {critics_rating.count} critics[/dim]",
        )
        console.print()

    if info.directors:
        console.print(f"[bold]Directors:[/bold] {_join_names(info.directors)}")

    if info.main_cast:
        console.print(f"[bold]Main cast:[/bold] {_join_names(info.main_cast)}")

    if full_desc:
        console.print()
        clean_full_description = " ".join(description.text.split())
        console.print(clean_full_description)
    elif info.description:
        console.print()
        clean_description = " ".join(info.description.split())
        console.print(clean_description)


def _format_count(count: int) -> str:
    return f"{count / 1000:.0f}k ratings" if count >= THOUSAND_THRESHOLD else str(count)


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
